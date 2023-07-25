from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_social_auth.views import SocialSessionAuthView
from django.contrib.auth.models import Group
from urllib.request import urlopen
from django.core.files import File
import tempfile
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .cnpj_validation import cnpj_validation

from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, AddressSerializer, User_fileSerializer, UserUpdateSerializer
from ..models import Address, User_file, User
from newdve_back.announces.models import Announcement
from newdve_back.announces.models import Tag

class AddresViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class User_fileViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = User_file.objects.all()
    serializer_class = User_fileSerializer

class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet, CreateModelMixin, DestroyModelMixin):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        print(request.data)
        subdata = {}
        for data in request.data:
            if request.data[data] != None:
                subdata[data] = request.data[data]

        files = []
        cnt = 0
        for key in request.data:
            if key.startswith(f"files[{cnt}]"):
                if key == f"files[{cnt}][id]":
                    files.append(User_file.objects.get(id=request.data[f"files[{cnt}][id]"]))
                    cnt += 1
                else:
                    pass
            if key == f"files[{cnt}]":
                files.append(request.data[f"files[{cnt}]"])
                cnt += 1
            if key == "files[]":
                files.append(request.data[f"files[]"])
        
        address, created = Address.objects.get_or_create(cep=request.data['cep'],district=request.data['district'],number=request.data['number'],street=request.data['street'],city=request.data['city'],state=request.data['state'])
        keys = ['cep','district','number','street','city','state']
        for key in keys:
            subdata.pop(key)

        subdata['address'] = address.id
        if 'birth_date' in subdata:
            data_obj = datetime.strptime(subdata['birth_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            data_formatada = data_obj.strftime('%d/%m/%Y')
            subdata['birth_date'] = data_formatada

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UserUpdateSerializer(instance, data=subdata, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if "tags[]" in request.data:
            tags = Tag.objects.filter(id__in=request.data.getlist('tags[]'))
            instance.preference_tags.set(tags)
            instance.save()
        
        userFiles = User_file.objects.filter(user=request.user)
        for file in userFiles:
            if file not in files:
                file.delete()
        for file in files:
            if file not in userFiles:
                User_file.objects.create(user=request.user, file=file)

        
        user = User.objects.get(id=request.user.id)
        refresh = RefreshToken.for_user(user)
            
        serializer = UserSerializer(user, context={'refresh' : str(refresh), 'access': str(refresh.access_token), "request": request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = Group.objects.get(name=request.data['groups'])
        if group.name == "Company":
            if not 'cnpj' in request.data:
                return Response({"Error": "CNPJ is required to company type users."}, status=status.HTTP_400_BAD_REQUEST)
            else: 
                cnpj = serializer.validated_data['cnpj']
                data = cnpj_validation(cnpj)
                if data['status'] == 'ERROR':
                    return Response({"Error": "Invalid CNPJ"}, status=status.HTTP_400_BAD_REQUEST)
                else: 
                    address, created = Address.objects.get_or_create(state=data['uf'],city=data['municipio'],district=data['bairro'],street=data['logradouro'],number=data['numero'],cep=data['cep'])
                    serializer.validated_data['address'] = address
                    serializer.validated_data['phone'] = data['telefone']
                    serializer.validated_data['name'] = data['nome']

        self.perform_create(serializer)

        user = User.objects.get(email=serializer.validated_data['email'])
        user.groups.add(group)
        user.set_password(request.data['password'])
        user.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'], detail=True, url_path='inscripts')
    def inscripts(self, request, *args, **kwarg):
        user = self.get_object()
        announces = Announcement.objects.filter(creator=user)
        total = 0
        for a in announces:
            total += a.inscripts.all().count()
        return Response(total, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='schooling')
    def schoolings(self, request, *args, **kwarg):
        return Response(User.SCHOOLING_CHOICES)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    @action(methods=['POST'],detail=False)
    def suap(self,request):
        user = request.data['user']
        try: 
            suap_student = User.objects.get(registration_ifrn=user["matricula"])
            refresh = RefreshToken.for_user(suap_student)
            
            serializer = UserSerializer(suap_student, context={'refresh' : str(refresh), 'access': str(refresh.access_token), 'request' : request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            User.objects.create(
                email = user['email'],
                name = user['nome_usual'],
                registration_ifrn = user['matricula'],
                birth_date = user['data_nascimento'],
                course = user['vinculo']['curso']
            )
            student = User.objects.get(registration_ifrn=user['matricula'])
            student.set_unusable_password()
            with urlopen(f"https://suap.ifrn.edu.br{user['url_foto_150x200']}") as uo:
                assert uo.status == 200
                with tempfile.NamedTemporaryFile(delete=True) as img_tmp:
                    img_tmp.write(uo.read())
                    img_tmp.flush()
                    img = File(img_tmp)
                    student.profile_picture.save(f'image_{student.name}.png', img)
                    student.save()
            group = Group.objects.get(name='IFRN_candidate')
            student.groups.add(group)
            student.save()

            refresh = RefreshToken.for_user(student)

            serializer = UserSerializer(student, context={'refresh' : str(refresh), 'access': str(refresh.access_token), 'request' : request})
            return Response(serializer.data, status=status.HTTP_200_OK)