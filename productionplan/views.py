from json import dumps as json_dumps, loads as json_loads

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


class FinalCheck(ValueError):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        e = 'Final check must be null. %s != 0' % self.data
        return e


class WrongPowerplantType(ValueError):
    def __init__(self, _type):
        self.type = _type

    def __str__(self):
        e = 'Type of powerplants: "%s" is not correct. [gasfired, turbojet, windturbine]' % self.type
        return e


class Powerplant:
    # noinspection PyShadowingBuiltins
    def __init__(self, fuels, name, type, efficiency, pmin, pmax):
        self.name = name
        self.type = type
        self.efficiency = efficiency
        self.pmin = self.real_pmin = pmin
        self.pmax = self.real_pmax = pmax
        self.price_mwh = self.percentage_wind = self.p = 0

        # calculate mwh price for sorting & real_pmax based on percentage_wind
        if self.type == 'turbojet':
            self.fuel_name = 'kerosine(euro/MWh)'
            self.fuel_data = fuels[self.fuel_name]
            self.price_mwh = round(self.fuel_data / self.efficiency, 2)
        elif self.type == 'windturbine':
            self.fuel_name = 'wind(%)'
            self.percentage_wind = fuels[self.fuel_name]
            self.real_pmax = pmax * self.percentage_wind / 100
        elif self.type == 'gasfired':
            self.fuel_name = 'gas(euro/MWh)'
            self.fuel_data = fuels[self.fuel_name]
            self.price_mwh = round(self.fuel_data / self.efficiency, 2)
        else:  # if type not corresponding on [gasfired, turbojet, windturbine], kill process
            raise WrongPowerplantType(self.type)

        self.r = self.real_pmax  # initialise residual value "r"

    def increase_p(self, i):
        """ Function to maintain obj values """
        self.p += i  # add value to final "p" value
        self.r -= i  # reduce residual value


class Payload:
    def __init__(self, load, fuels, powerplants):
        self.load = load
        self.powerplants = [Powerplant(fuels=fuels, **el) for el in powerplants]
        # sort powerplants on price_mwh attribute
        self.sorted_powerplants = sorted(self.powerplants, key=lambda x: x.price_mwh)

    def generate(self):
        """ calculate which powerplant to use and generate de data to return as json """
        load = self.load  # copy load value to work with
        # first get all pmin for each powerplants
        for powerplant in self.sorted_powerplants:
            if powerplant.real_pmin:
                load -= powerplant.real_pmin
                powerplant.increase_p(powerplant.real_pmin)

        for powerplant in self.sorted_powerplants:
            if load == 0:
                continue
            elif load > powerplant.r:
                load -= powerplant.r
                powerplant.increase_p(powerplant.r)
            else:
                powerplant.increase_p(load)
                load = 0

        data = [{'name': el.name, 'p': round(el.p, 1) if el.p > 0 else 0} for el in self.sorted_powerplants]

        # check results with sum of all p in powerplant obj
        _ = sum([el['p'] for el in data]) - self.load
        if _ != 0:
            raise FinalCheck(_)

        return data


@csrf_exempt
@require_http_methods(['POST'])
def post_rest_api(request):
    """ main rest API """
    payload = json_loads(request.body.decode('utf-8'))
    payload = Payload(**payload)
    data = payload.generate()
    return HttpResponse(json_dumps(data), content_type='application/json')
