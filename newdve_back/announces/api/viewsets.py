from datetime import datetime
from rest_framework import viewsets, status
from django.core.files.base import ContentFile
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from newdve_back.users.models import Address, User
from newdve_back.announces.models import Announcement, Tag, Announcement_image, Rating
from newdve_back.announces.api.serializers import AnnouncementSerializer, TagSerializer, Announcement_imageSerializer, RatingSerializer, SimpleAnnouncementSerializer, AnnounceCreateSerializer

class AnnounceViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search') or False
        tags = request.query_params.get('tags') or False
        order = request.query_params.get('order') or False
        rentable = request.query_params.get('rentable') or False

        if order:
            queryset = Announcement.objects.all().order_by(f"-{order}")
        else:
            queryset = Announcement.objects.all()
        if search:
            queryset = queryset.filter(company_name__icontains=search)
        if tags:
            tags = str(tags.replace(",", ""))
            list_tags = Tag.objects.filter(id__in=tags)
            for tag in list_tags:
                ids = list(Announcement.objects.filter(tags__id=tag.id).values_list("id",flat=True))
                queryset = queryset.filter(id__in=ids)
        if rentable:
            queryset = queryset.filter(salary__gt=0)

        if request.user.groups.filter(name="Company").count() != 1:
            now = datetime.now()
            queryset = queryset.filter(deadline__gt=now)

        page = self.paginate_queryset(queryset)
        if page is not None: 
            serializer = SimpleAnnouncementSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SimpleAnnouncementSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        print(request.data)
        subdata = {}
        for data in request.data:
            if request.data[data] != None:
                subdata[data] = request.data[data]

        images = []
        cnt = 0
        for key in request.data:
            if key.startswith(f"images[{cnt}]"):
                if key == f"images[{cnt}][id]":
                    images.append(Announcement_image.objects.get(id=request.data[f"images[{cnt}][id]"]))
                    cnt += 1
                else:
                    pass
            if key == f"images[{cnt}]":
                images.append(request.data[f"images[{cnt}]"])
                cnt += 1
            if key == "images[]":
                images.append(request.data[f"images[]"])
        print(images)

        address, created = Address.objects.get_or_create(cep=request.data['CEP'],district=request.data['district'],number=request.data['number'],street=request.data['street'],city=request.data['city'],state=request.data['state'])
        keys = ['CEP','district','number','street','city','state']
        for key in keys:
            subdata.pop(key)
            
        subdata['address'] = address.id
        data_obj = datetime.strptime(subdata['deadline'], '%Y-%m-%dT%H:%M:%S.%fZ')
        data_formatada = data_obj.strftime('%d/%m/%Y')
        subdata['deadline'] = data_formatada

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = AnnounceCreateSerializer(instance, data=subdata, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if "tags[]" in request.data:
            tags = Tag.objects.filter(id__in=request.data.getlist('tags[]'))
            instance.tags.set(tags)
            instance.save()

        announceImages = Announcement_image.objects.filter(announcement=instance)
        for image in announceImages:
            if image not in images:
                image.delete()
        for image in images:
            if image not in announceImages:
                Announcement_image.objects.create(announcement=instance, image=image)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print(request.data)
        subdata = request.data

        address, created = Address.objects.get_or_create(cep=request.data['CEP'],district=request.data['district'],number=request.data['number'],street=request.data['street'],city=request.data['city'],state=request.data['state'])
        keys = ['CEP','district','number','street','city','state']
        for key in keys:
            subdata.pop(key)
            
        subdata['address'] = address.id
        data_obj = datetime.strptime(subdata['deadline'], '%Y-%m-%dT%H:%M:%S.%fZ')
        data_formatada = data_obj.strftime('%d/%m/%Y')
        subdata['deadline'] = data_formatada

        if "tags[]" in request.data:
            tags = Tag.objects.filter(Q(id__in=request.data.getlist('tags[]'))|Q(tag_name='Novo'))
        else: 
            tags = Tag.objects.filter(tag_name='Novo')

        serializer = self.get_serializer(data=request.data)
        creator = request.user
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['address'] = address
        serializer.validated_data['creator'] = creator
        serializer.validated_data['tags'] = tags
        self.perform_create(serializer)

        announce = Announcement.objects.filter(creator=request.user).last()
        for image in request.data.getlist('images[]'):
            Announcement_image.objects.create(announcement=announce, image=image)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['post'], detail=True, url_path='save_unsave')
    def save_unsave(self, request, *args, **kwarg):
        announcement = self.get_object()
        user = request.user

        if announcement.id in user.saved_announcements.values_list('id', flat=True):
            user.saved_announcements.remove(announcement)
            return Response({'Action':'removed'},status=status.HTTP_200_OK)
        else:
            user.saved_announcements.add(announcement)
            return Response({'Action':'saved'},status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=True, url_path='subscribe_unsubscribe')
    def subscribe_unsubscribe(self, request, *args, **kwarg):
        announcement = self.get_object()
        user = request.user

        if user.id in announcement.inscripts.values_list('id', flat=True):
            announcement.inscripts.remove(user)
            return Response({'Action':'unsubscribed'},status=status.HTTP_200_OK)
        else:
            announcement.inscripts.add(user)
            return Response({'Action':'subscribed'},status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='courses')
    def courses(self, request, *args, **kwarg):
        return Response(Announcement.COURSE_CHOICES)
    
class TagViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class Announce_imageViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Announcement_image.objects.all()
    serializer_class = Announcement_imageSerializer

class RatingViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        announce = Announcement.objects.get(id=request.data['announcement'])
        try:
            Rating.objects.get(user=request.user, announcement = announce).delete()
        except Rating.DoesNotExist:
            pass

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        rate = Rating.objects.all().latest('id')
        rate.user = self.request.user
        rate.announcement = announce
        rate.save()

        rates = Rating.objects.filter(announcement=announce).values_list("rate",flat=True)
        total = 0
        for rating in rates:
            total += rating
        announce.rate = total/rates.count()
        announce.save()

        print(rate)
        serializer = RatingSerializer(rate)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


