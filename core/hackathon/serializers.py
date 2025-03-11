from rest_framework import serializers
from .models import Hackathon, Tag, PrizePlaces, Track, Team, Solution, SolutionReview, FAQ, LiveStream
from user.serializers import UserSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']

class TrackSerializer(serializers.ModelSerializer):
    participants_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Track
        fields = ['id', 'hackathon', 'name', 'description', 'task_description', 'max_participants', 'participants_count']

class TeamSerializer(serializers.ModelSerializer):
    leader = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    members_count = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'hackathon', 'track', 'leader', 'members',
            'max_members', 'join_code', 'status', 'created_at',
            'members_count', 'is_full'
        ]

class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'hackathon', 'track', 'max_members', 'status']
    
    def create(self, validated_data):
        user = self.context['request'].user
        team = Team.objects.create(leader=user, **validated_data)
        team.members.add(user)
        return team

class SolutionReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    
    class Meta:
        model = SolutionReview
        fields = ['id', 'solution', 'reviewer', 'rating', 'comment', 'created_at']

class SolutionSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    reviews = SolutionReviewSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Solution
        fields = [
            'id', 'hackathon', 'track', 'team', 'user', 'title', 'description',
            'repository_url', 'demo_url', 'presentation_url', 'status',
            'submitted_at', 'reviews', 'average_rating'
        ]

class SolutionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = [
            'hackathon', 'track', 'team', 'title', 'description',
            'repository_url', 'demo_url', 'presentation_url'
        ]
    
    def create(self, validated_data):
        user = self.context['request'].user
        solution = Solution.objects.create(user=user, status='draft', **validated_data)
        return solution

class SolutionReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionReview
        fields = ['solution', 'rating', 'comment']
    
    def create(self, validated_data):
        user = self.context['request'].user
        review = SolutionReview.objects.create(reviewer=user, **validated_data)
        return review

class PrizePlacesSerializer(serializers.ModelSerializer):
    winner = UserSerializer(read_only=True)
    winner_team = TeamSerializer(read_only=True)
    
    class Meta:
        model = PrizePlaces
        fields = ['id', 'hackathon', 'place', 'prize_amount', 'winner', 'winner_team']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'hackathon', 'question', 'answer']

class LiveStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveStream
        fields = ['id', 'hackathon', 'title', 'stream_url', 'start_time', 'end_time', 'is_active']

class HackathonSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    prize_places = PrizePlacesSerializer(many=True, read_only=True)
    tracks = TrackSerializer(many=True, read_only=True)
    faqs = FAQSerializer(many=True, read_only=True)
    live_streams = LiveStreamSerializer(many=True, read_only=True)
    organizer = UserSerializer(read_only=True)
    judges = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Hackathon
        fields = [
            'id', 'name', 'description', 'type', 'participation_type',
            'start_registation', 'end_registration', 'anonce_start',
            'start_hackathon', 'end_hackathon', 'submission_deadline',
            'image', 'created_at', 'status', 'prize_pool', 'number_of_winners',
            'participants_count', 'tags', 'prize_places', 'tracks', 'faqs',
            'live_streams', 'max_team_size', 'organizer', 'location', 'rules',
            'program', 'judges', 'enable_public_voting', 'show_solutions_after_deadline',
            'xp_reward_participation', 'xp_reward_winner', 'crystal_reward_winner'
        ]

class HackathonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = [
            'name', 'description', 'type', 'participation_type',
            'start_registation', 'end_registration', 'anonce_start',
            'start_hackathon', 'end_hackathon', 'submission_deadline',
            'image', 'prize_pool', 'number_of_winners', 'max_team_size',
            'location', 'rules', 'program', 'enable_public_voting',
            'show_solutions_after_deadline', 'xp_reward_participation',
            'xp_reward_winner', 'crystal_reward_winner'
        ]
    
    def create(self, validated_data):
        user = self.context['request'].user
        hackathon = Hackathon.objects.create(organizer=user, **validated_data)
        return hackathon 