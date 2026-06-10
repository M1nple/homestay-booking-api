from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from bookings.models import Booking, BookingRoom
from rooms.models import Room
from homestays.models import Homestay

class BookingRoomInputSerializer(serializers.Serializer):

    room = serializers.PrimaryKeyRelatedField( #PrimaryKeyRelatedField là một trường đặc biệt trong Django REST Framework được sử dụng để liên kết một đối tượng với một đối tượng khác thông qua khóa chính (primary key). Nó cho phép bạn chỉ định một đối tượng liên quan bằng cách sử dụng giá trị của khóa chính của nó.
        queryset=Room.objects.filter(
            deleted_at__isnull=True,
            homestay__deleted_at__isnull=True
        )
    )

class BookingRoomSerializer(serializers.ModelSerializer):

    room_name = serializers.CharField(
        source='room.name',
        read_only=True
    )

    class Meta:
        model = BookingRoom
        fields = [
            'room',
            'room_name',
            'price',
        ]

class BookingSerializer(serializers.ModelSerializer):

    rooms = BookingRoomSerializer(
        # source='bookingroom_set', # BỎ
        many=True,
        read_only=True
    )
    homestay_name = serializers.CharField(
        source='homestay.name',
        read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            # 'homestay',
            'id',
            'homestay_name',
            'check_in',
            'check_out',
            'total_guests',
            'total_price',
            'status',
            'rooms',
        ]

class CreateBookingSerializer(serializers.ModelSerializer):
    rooms = BookingRoomInputSerializer(
        many=True,
        write_only=True
    )
    class Meta:
        model = Booking
        fields = [
            'homestay',
            'check_in',
            'check_out',
            'total_guests',
            'rooms'
        ]
    def validate(self, data):
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        total_guests = data.get('total_guests')
        rooms = data.get('rooms')
        # validate date
        if check_in and check_out and check_in >= check_out:
            raise serializers.ValidationError(
                "Ngày trả phòng phải sau ngày nhận phòng."
            )
        # validate guests
        if total_guests is not None and total_guests <= 0:
            raise serializers.ValidationError(
                "Số lượng khách phải lớn hơn 0."
            )
            # tổng sức chứa các phòng
        total_capacity = sum(
            item['room'].capacity
            for item in rooms)
        if total_guests > total_capacity:
            raise serializers.ValidationError(
                f'Tổng số khách ({total_guests}) vượt quá sức chứa của các phòng ({total_capacity}).')
        # validate room conflict
        for item in rooms:
            room = item['room']
            conflict = BookingRoom.objects.filter( # Query tìm booking overlap.
                room=room,
                booking__check_in__lt=check_out,
                booking__check_out__gt=check_in,
                booking__status__in=[
                    Booking.Status.PENDING,
                    Booking.Status.CONFIRMED
                ]
            ).exists()
            if conflict:
                raise serializers.ValidationError(
                    f'Phòng "{room.name}" đã được đặt trong khoảng thời gian này.'
                )
        return data

    def create(self, validated_data):
        rooms_data = validated_data.pop('rooms')
        user = self.context['request'].user
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']
        days = (check_out - check_in).days
        total_price = 0
        booking = Booking.objects.create(
            user=user,
            total_price=0,
            expired_at=timezone.now() + timedelta(minutes=15),
            **validated_data
        )
        for item in rooms_data:
            room = item['room']
            room_price = room.price * days
            total_price += room_price
            BookingRoom.objects.create(
                booking=booking,
                room=room,
                price=room.price
            )
        booking.total_price = total_price
        booking.save()
        return booking
 
class BookingDetailSerializer(serializers.ModelSerializer):

    rooms = BookingRoomSerializer(
        many=True,
        read_only=True
    )

    homestay_name = serializers.CharField(
        source='homestay.name',
        read_only=True
    )

    user_name = serializers.CharField(
        source='user.email',
        read_only=True
    )
    class Meta:
        model = Booking
        fields = [
            'id',
            'user_name',
            'homestay_name',
            'check_in',
            'check_out',
            'total_guests',
            'total_price',
            'status',
            'rooms',
            'created_at',
            'expired_at'

        ]
