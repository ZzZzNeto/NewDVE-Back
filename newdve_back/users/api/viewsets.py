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
from .serializers import UserSerializer, AddressSerializer, User_fileSerializer
from ..models import Address, User_file

User = get_user_model()

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
            
            serializer = UserSerializer(suap_student, context={'refresh' : str(refresh), 'access': str(refresh.access_token)})
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

            serializer = UserSerializer(student, context={'refresh' : str(refresh), 'access': str(refresh.access_token)})
            return Response(serializer.data, status=status.HTTP_200_OK)