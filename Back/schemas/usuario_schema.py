import re
from marshmallow import Schema, fields, validate, ValidationError
from extensions import ma


def validar_rut(rut):
    patron = re.compile(r'^\d{7,8}-[\dkK]$')
    if not patron.match(rut):
        raise ValidationError('Ingrese RUT en formato XXXXXXXX-X')


def validar_telefono(telefono):
    patron = re.compile(r'^(\+56)?9\d{8}$')
    if not patron.match(telefono):
        raise ValidationError('Ingrese un numero valido')


class UsuarioRegistroSchema(Schema):
    nombres = fields.Str(required=True, validate=validate.Length(min=1))
    apellidos = fields.Str(required=True, validate=validate.Length(min=1))
    foto_url = fields.Str(allow_none=True)
    descripcion = fields.Str(allow_none=True)
    direccion = fields.Str(allow_none=True)
    fecha_nacimiento = fields.Date(required=True, format='%d-%m-%Y')
    rut = fields.Str(required=True, validate=validar_rut)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    telefono = fields.Str(required=True, validate=validar_telefono)
    instagram_url = fields.Str(allow_none=True)
    facebook_url = fields.Str(allow_none=True)
    web_url = fields.Str(allow_none=True)


class UsuarioPerfilPrivadoSchema(ma.Schema):
    class Meta:
        fields = ('id',
                  'nombres',
                  'apellidos',
                  'fecha_nacimiento',
                  'rut',
                  'email',
                  'telefono',
                  'rol_id',
                  'foto_url',
                  'descripcion',
                  'direccion',
                  'web_url',
                  'instagram_url',
                  'facebook_url',
                  'creado_en',
                  'actualizado_en')


class UsuarioPerfilPublicoSchema(ma.Schema):
    class Meta:
        fields = ('id',
                  'nombres',
                  'apellidos',
                  'foto_url',
                  'descripcion',
                  'telefono',
                  'rol_id',
                  'web_url',
                  'instagram_url',
                  'facebook_url')


perfil_privado_schema = UsuarioPerfilPrivadoSchema()
perfil_publico_schema = UsuarioPerfilPublicoSchema()


class UsuarioEdicionSchema(Schema):
    nombres = fields.Str(validate=validate.Length(min=1))
    apellidos = fields.Str(validate=validate.Length(min=1))
    telefono = fields.Str(validate=validar_telefono)
    descripcion = fields.Str(allow_none=True)
    direccion = fields.Str(allow_none=True)
    web_url = fields.Str(allow_none=True)
    instagram_url = fields.Str(allow_none=True)
    facebook_url = fields.Str(allow_none=True)
    foto_url = fields.Str(allow_none=True)
