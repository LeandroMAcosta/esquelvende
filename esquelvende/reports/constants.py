# -*- coding: utf-8 -*-
REASON_CHOICES = (
    ('FLS', 'Vende una copia o una falsificacion'),
    ('TRM', 'No cumple los Terminos y Condiciones del sitio'),
    ('OTR', 'Otros')
)

# Notificar moderador

MODNOTIFICATION = 1

# Eliminar producto

DELPRODUCT = 2

# Email

SUBJECT_USER = 'Esquel Vende'
MESSAGE_USER = 'Su producto ha sido eliminado por no respetar las politicas\
                y condiciones de Esquel Vende\n'


SUBJECT_MOD = 'Producto o servicio reportado'
MESSAGE_MOD = 'Revisar el producto con Id: '
