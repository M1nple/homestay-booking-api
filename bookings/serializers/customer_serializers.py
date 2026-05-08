from rest_framework import serializers
from bookings.models import Booking, BookingRoom
from rooms.models import Room

class BookingRoomInputSerializer(serializers.Serializer):

    room = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.filter(
            deleted_at__isnull=True
        )
    )

    quantity = serializers.IntegerField(min_value=1)

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
        check_in = data.get('check_in') # lấy ngày nhận phòng từ dữ liệu đã được xác thực (validated data)
        check_out = data.get('check_out') # lấy ngày trả phòng từ dữ liệu đã được xác thực (validated data)
        total_guests = data.get('total_guests')  # lấy số lượng khách từ dữ liệu đã được xác thực (validated data)
        
        if check_in and check_out and check_in >= check_out:
            raise serializers.ValidationError("Ngày trả phòng phải sau ngày nhận phòng.")
        
        if total_guests is not None and total_guests <= 0:
            raise serializers.ValidationError("Số lượng khách phải lớn hơn 0.")
        
        if check_in and check_out:
            conflict = Booking.objects.filter( 
                homestay=data['homestay'], # chỉ kiểm tra booking của đúng homestay đó.
                check_in__lt=check_out, #lt = less than (<)
                check_out__gt=check_in, # gt = greater than (>)
                status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED] # chỉ kiểm tra những booking có trạng thái PENDING hoặc CONFIRMED, 
            ).exists() # exists() trả về True hoặc false nếu có tồn tại booking nào trùng lịch hay không

            if conflict:
                raise serializers.ValidationError("Khoảng thời gian này đã có người đặt. Vui lòng chọn khoảng thời gian khác.")
        return data
    
    def create(self, validated_data):
        rooms_data = validated_data.pop('rooms') # lấy thông tin phòng từ dữ liệu đã được xác thực (validated data) và loại bỏ nó khỏi validated_data
        user = self.context['request'].user
        days = (validated_data['check_out'] - validated_data['check_in']).days # tính tổng giá dựa trên số đêm và số khách
        total_price = 0

        booking = Booking.objects.create(
            user=user,
            total_price=0,
            **validated_data
        )

        for item in rooms_data:
            room = item['room']
            quantity = item['quantity']
            room_price = room.price * quantity * days
            total_price += room_price

        booking.total_price = total_price
        booking.save()

        return booking

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
            'quantity',
            'price',
        ]

class BookingDetailSerializer(serializers.ModelSerializer):

    rooms = BookingRoomSerializer(
        source='bookingroom_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Booking
        fields = '__all__'