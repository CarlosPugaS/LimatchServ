from marshmallow import Schema, fields, validate, ValidationError
import re

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
  apellidos = fields.Str(requiered=True, validate=validate.Length(min=1))
  fecha_nacimiento = fields.Date(required=True, format='%d-%m-%Y')
  rut = fields.Str(requiered=True, validate=validar_rut)
  email = fields.Email(required=True)
  password = fields.Str(required=True, validate=validate.Length(min=6))
  telefono = fields.Str(required=True, validate=validar_telefono)
  instagram_url = fields.Str(allow_none=True)
  facebook_url = fields.Str(allow_none=True)