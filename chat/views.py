from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import ChatMessage
from .serializers import MessageSerializer

# Create your views here.
class GetChatMessages(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, room_id):
        try:
            print("The room id is : ", room_id)
            messages = ChatMessage.objects.filter(room_name=room_id).order_by("timestamp")
            print("The messages are :", messages )
            serializer = MessageSerializer(messages, many=True)
            print("The serialized messages are :", serializer.data )
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print("The error is : ", e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)