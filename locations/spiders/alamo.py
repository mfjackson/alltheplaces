# -*- coding: utf-8 -*-
import json
import scrapy

from locations.items import GeojsonPointItem


class AlamoSpider(scrapy.Spider):
    name = "alamo"
    allowed_domains = ["alamo.com"]

    def start_requests(self):
        yield scrapy.Request(
            "https://prd.location.enterprise.com/enterprise-sls/search/location/alamo/web/all?cor=US&dto=true",
        )

    def parse(self, response):
        loc_data = json.loads(response.body_as_unicode())

        for loc in loc_data:

            properties = {
                "name": loc["name"],
                "brand": loc["brand"],
                "phone": loc["phones"][0]["phone_number"],
                "addr_full": loc["address"]["street_addresses"],
                "city": loc["address"].get("city"),
                "state": loc["address"]["country_subdivision_code"],
                "postcode": loc["address"]["postal"],
                "country": loc["address"].get("country_code"),
                "lat": float(loc["gps"]["latitude"]),
                "lon": float(loc["gps"]["longitude"]),
                "ref": loc["id"],
            }

            yield GeojsonPointItem(**properties)
