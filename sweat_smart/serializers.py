from rest_framework import serializers

class StravaStatsRequestSerializer(serializers.Serializer):
    """Serializer for validating Strava stats request parameters."""
    
    athlete_id = serializers.CharField(
        required=True,
        help_text="Strava athlete ID"
    )
    access_token = serializers.CharField(
        required=True,
        help_text="Strava access token"
    )
    
    def validate_athlete_id(self, value):
        """Validate that athlete_id is numeric."""
        try:
            int(value)
        except ValueError:
            raise serializers.ValidationError("Athlete ID must be numeric")
        return value

class WorkoutRecommendationSerializer(serializers.Serializer):
    """Serializer for workout recommendation responses."""
    
    pace = serializers.CharField()
    time = serializers.FloatField()
    suggested = serializers.BooleanField()
    title = serializers.CharField()
    difficulty = serializers.CharField()
    pace_unit = serializers.CharField()
    workout_plan = serializers.CharField()

class WorkoutCollectionSerializer(serializers.Serializer):
    """Serializer for collections of workout recommendations."""
    
    rides = WorkoutRecommendationSerializer(many=True)
    runs = WorkoutRecommendationSerializer(many=True)
    swims = WorkoutRecommendationSerializer(many=True)

class StravaStatsResponseSerializer(serializers.Serializer):
    """Serializer for Strava stats response."""
    
    workouts = WorkoutCollectionSerializer()
    recent_workout_type = serializers.CharField(allow_null=True)
