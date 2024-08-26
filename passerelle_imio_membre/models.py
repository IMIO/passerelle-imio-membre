import json

import requests
from django.db import models
from passerelle.base.models import BaseResource
from passerelle.utils.api import endpoint
from django.conf import settings


class ConnectorMembre(BaseResource):
    """
    Connector Membre
    """
    api_description = "Connecteur pour les membres iMio"
    category = "Connecteurs iMio"

    class Meta:
        verbose_name = "Connecteur pour l'espace Membre"

    username = models.CharField(
        max_length=128,
        blank=False,
        verbose_name="Username",
        help_text="Username pour l''API",
    )

    password = models.CharField(
        max_length=128,
        blank=False,
        verbose_name="Mot de passe",
        help_text="Mot de passe pour l''API",
    )

    slug_card = models.CharField(
        max_length=128,
        blank=False,
        verbose_name="Slug des fiches",
        help_text="Slug des fiches membre",
    )

    @endpoint(
        name="membre",
        perm="can_access",
        methods=["get"],
        description="Liste fiches membres",
        long_description="Permet d'avoir la liste des fiches de membres",
        display_order=1,
        display_category="MEMBRES",
        pattern="^list",
        example_pattern="list",
    )
    def get_membres(self, request,):
        username = self.username
        password = self.password
        if not getattr(settings, "KNOWN_SERVICES", {}).get("wcs"):
            return "error"
        eservices = list(settings.KNOWN_SERVICES["wcs"].values())[0]['url']

        url = f"{eservices}api/cards/{self.slug_card}/list"
        headers = {"Content-Type": "application/json"}
        auth = (username, password)

        response = requests.get(url=url, headers=headers, auth=auth)
        response.raise_for_status()

        return response.json()

    @endpoint(
        name="membre",
        perm="can_access",
        methods=["get"],
        description="Get fiche membre",
        long_description="Permet de chercher des fiches de membres",
        display_order=2,
        display_category="MEMBRES",
        pattern="^get",
        example_pattern="get",
        parameters={
            "organisation": {
                "description": "organisation du user",
                "example_value": "0841470248",
            },
        },
    )
    def get_fiche_membre(self, request, organisation=None):
        username = self.username
        password = self.password
        if not getattr(settings, "KNOWN_SERVICES", {}).get("wcs"):
            return "error"
        eservices = list(settings.KNOWN_SERVICES["wcs"].values())[0]['url']

        url = f"{eservices}api/cards/{self.slug_card}/list"
        headers = {"Content-Type": "application/json"}
        auth = (username, password)
        payload = {"filter-organisation": organisation}

        response = requests.get(url=url, headers=headers, auth=auth, params=payload)
        response.raise_for_status()

        return response.json()
