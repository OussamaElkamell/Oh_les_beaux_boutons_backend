from rest_framework import serializers
from .models import GameResult, GameChoice, WrongAnswer


class GameChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameChoice
        fields = ['card_id', 'card_name', 'card_type', 'accepted', 'points_earned', 'timestamp']


class WrongAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrongAnswer
        fields = ['card_id', 'card_name', 'card_type', 'alternative_name', 'reason', 'recommendation']


class GameResultSerializer(serializers.ModelSerializer):
    choices = GameChoiceSerializer(many=True, read_only=True)
    wrong_answers = WrongAnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = GameResult
        fields = [
            'id', 'nird_score', 'total_points',
            'inclusion_score', 'responsabilite_score', 'durabilite_score',
            'total_savings_euros', 'total_savings_co2',
            'cards_played', 'correct_choices',
            'started_at', 'completed_at',
            'choices', 'wrong_answers'
        ]


class GameResultCreateSerializer(serializers.ModelSerializer):
    choices = GameChoiceSerializer(many=True)
    wrong_answers = WrongAnswerSerializer(many=True, required=False)
    
    class Meta:
        model = GameResult
        fields = [
            'nird_score', 'total_points',
            'inclusion_score', 'responsabilite_score', 'durabilite_score',
            'total_savings_euros', 'total_savings_co2',
            'cards_played', 'correct_choices',
            'started_at', 'choices', 'wrong_answers'
        ]
    
    def create(self, validated_data):
        choices_data = validated_data.pop('choices', [])
        wrong_answers_data = validated_data.pop('wrong_answers', [])
        
        # Get user from context if authenticated
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        
        game_result = GameResult.objects.create(**validated_data)
        
        # Create choices
        for choice_data in choices_data:
            GameChoice.objects.create(game_result=game_result, **choice_data)
        
        # Create wrong answers
        for wrong_answer_data in wrong_answers_data:
            WrongAnswer.objects.create(game_result=game_result, **wrong_answer_data)
        
        # Update user profile if authenticated
        if game_result.user and hasattr(game_result.user, 'profile'):
            profile = game_result.user.profile
            profile.total_games_played += 1
            profile.total_points_earned += game_result.total_points
            if game_result.nird_score > profile.best_nird_score:
                profile.best_nird_score = game_result.nird_score
            profile.save()
        
        return game_result


class GameResultListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    
    class Meta:
        model = GameResult
        fields = ['id', 'nird_score', 'total_points', 'cards_played', 'completed_at']
