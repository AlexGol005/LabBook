from kinematicviscosity.models import ViscosityMJL
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


from .models import LotVG, VGrange

@receiver(post_save, sender=ViscosityMJL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            tryname = VGrange.objects.get(name=ViscosityMJL.name)
        except ObjectDoesNotExist:
            tryname = None

        try:
            trylot = LotVG.objects.get(lot=ViscosityMJL.lot)
        except ObjectDoesNotExist:
            trylot = None

        if  (trylot and tryname):
            LotVG.objects.create(viscosity=instance)



        # if created:
        #     try:
        #         LotVG.objects.get(lot=1, nameVG__name='ВЖ-2-ПА(2)')
        #     except LotVG.DoesNotExist:
        #         LotVG.objects.create(viscosity=instance)





