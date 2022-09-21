from django.shortcuts import render
import json
from django.http import HttpResponse
from .serializers import *
from .models import  *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from .nwtracker import django_helpers
from rest_framework.authtoken.views import ObtainAuthToken

class StockTrxnList(generics.ListCreateAPIView):
    serializer_class = StockTrxnSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return StockTrxn.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class StockTrxnDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockTrxn.objects.all()
    serializer_class = StockTrxnSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

class CashEntryList(generics.ListCreateAPIView):
    serializer_class = CashEntrySerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return CashEntry.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CashEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CashEntry.objects.all()
    serializer_class = CashEntrySerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

class FullUserDetail(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserGetSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)

class AnalysisAcrossTime(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        req_aacr_serializer = AnalysisAcrossRequestSerializer(data=request.data)
        if req_aacr_serializer.is_valid():
            request_data = req_aacr_serializer.validated_data
            hasError = False
            try:
                analysis_data = django_helpers.pull_db_generate_analysis(request.user,
                                                                         request_data["date_bef"],
                                                                         request_data["date_aft"],
                                                                         request_data["currency"])

            except ValueError:
                hasError = True
            if hasError:
                return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                analysis_serializer = AnalysisAcrossResponseSerializer(data=analysis_data)
                if analysis_serializer.is_valid():
                    return Response(analysis_serializer.data, status=status.HTTP_200_OK)
                return Response(analysis_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(req_aacr_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSignUp(ObtainAuthToken):
    def post(self, request, format=None):
        incoming_credentials_serializer = UserCreateSerializer(data=request.data)
        if incoming_credentials_serializer.is_valid():
            new_user = incoming_credentials_serializer.save()
            token, created = Token.objects.get_or_create(user=new_user)
            return Response({"token" : token.key})
        return Response(incoming_credentials_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

