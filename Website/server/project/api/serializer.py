from rest_framework import serializers
from .models import Username, LapTime, RaceSession


        
class LapTimeSerializer(serializers.ModelSerializer):
    lap_number = serializers.IntegerField()
    lap_time = serializers.DecimalField(max_digits=20, decimal_places=3)

    class Meta:
        model = LapTime
        fields = ['lap_number', 'lap_time']
    
class UsernameSerializer(serializers.ModelSerializer):
    lap_times = LapTimeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Username
        fields = ['id', 'user', 'lap_times']


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
    lap_times = LapTimeSerializer(many=True)

    def create(self, validated_data):
        # if isinstance(validated_data, list):
        #     result = []
        #     for item in validated_data:
        #         result.append(self.create(item))
        #     return result
        
        user_id = validated_data.get('user_id', None)
        username = validated_data.get('user', None)
        total_time = validated_data['total_time']
        laps_data = validated_data['lap_times']

        if user_id:
            try:
                user = Username.objects.get(pk=user_id)
            except Username.DoesNotExist:
                raise serializers.ValidationError("User with given ID does not exist")
        
        elif username:
            user, _ = Username.objects.get_or_create(user=username)
        else:
            raise serializers.ValidationError("Either user_id or user must be provided")
        
        LapTime.objects.filter(user=user).delete()

        fastest_lap = min(laps_data, key=lambda lap: lap['lap_time'])
                          
        LapTime.objects.create(
            user=user,
            lap_number=fastest_lap['lap_number'],
            lap_time=fastest_lap['lap_time'],
        )

        user.total_time = total_time
        user.save()

     
        return validated_data

    def update(self, instance, validated_data):
        print("DEBUG - validated_data", validated_data)
        total_time = validated_data.get('total_time', instance.total_time)
        laps_data = validated_data.get('lap_times', [])

        instance.total_time = total_time
        instance.save()

        LapTime.objects.filter(user=instance).delete()

        for lap_data in laps_data:
            LapTime.objects.create(
                user=instance,
                lap_number=lap_data['lap_number'],
                lap_time=lap_data['lap_time'],
            )

        return instance