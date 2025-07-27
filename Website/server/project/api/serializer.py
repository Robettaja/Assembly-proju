from rest_framework import serializers
from .models import Username, LapTime, RaceSession

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Username
        fields = '__all__'
        
class LapTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LapTime
        fields = ['lap_number', 'lap_time']

class RaceSessionSerializer(serializers.ModelSerializer):
    lap_times = LapTimeSerializer(many=True)
    user = serializers.IntegerField(write_only=True)

    class Meta:
        model = RaceSession
        fields = ['id', 'user', 'total_times', 'lap_times', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        lap_times_data = validated_data.pop('lap_times')
        username = validated_data.pop('user')
        user, _ = Username.objects.get_or_create(user=username)

        race_session = RaceSession.objects.create(user=user, **validated_data)

        for lap_data in lap_times_data:
            LapTime.objects.create(race_session=race_session, **lap_data)

        return race_session

class SaveLapsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    user = serializers.CharField(required=False)
    total_time = serializers.CharField()
    laps = LapTimeSerializer(many=True)

    def create(self, validated_data):
        user_id = validated_data.get('user_id', None)
        username = validated_data.get('user', None)
        total_time = validated_data['total_time']
        laps_data = validated_data['laps']

        if user_id:
            try:
                user = Username.objects.get(pk=user_id)
            except Username.DoesNotExist:
                raise serializers.ValidationError("User with given ID does not exist")
        
        elif username: 
            user, created = Username.objects.get_or_create(user=username)
        else:
            raise serializers.ValidationError("Either user_id or user must be provided")
        
        user.total_time = total_time
        user.save()



        for lap in laps_data:
            LapTime.objects.create(
                user=user,
                lap_number=lap['lap_number'],
                lap_time=lap['lap_time'],
            )

        return validated_data
