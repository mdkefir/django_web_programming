import json
from django.test import TestCase
from cars.models import Car, Brand, Owner, Service, ServiceRecord
from model_bakery import baker
from rest_framework.test import APIClient

# Create your tests here.
# mixin car
class CarsViewsetTestCase(TestCase):
    def test_get_list(self):
        brnd = baker.make("cars.Brand")
        car = baker.make("Car", brand=brnd)

        r = self.client.get("/api/cars/")
        data = r.json()
        print(data)

        assert car.name == data[0]['name']
        assert car.id == data[0]['id']
        assert car.brand.id == data[0]['brand']
        assert len(data) == 1

    def test_create_car(self):
       brnd = baker.make("cars.Brand")

       r = self.client.post("/api/cars/", {
           "name": "Corolla",
           "brand": brnd.id
       })

       new_car_id = r.json()['id']

       cars = Car.objects.all()
       assert len(cars) == 1

       new_car = Car.objects.filter(id=new_car_id).first()
       assert new_car.name == 'Corolla'
       assert new_car.brand == brnd

    def test_retrieve_car(self):
        client = APIClient()
        brand = Brand.objects.create(name="BMW")
        car = Car.objects.create(name="X5", brand=brand)
        response = client.get(f'/api/cars/{car.id}/')
        assert response.status_code == 200

    def test_update_car(self):
        cars = baker.make("Car", 10)
        car: Car = cars[2]

        r = self.client.get(f'/api/cars/{car.id}/')
        data = r.json()
        assert data['name'] == car.name

        r = self.client.put(
            f'/api/cars/{car.id}/',
            data=json.dumps({"name": "Новая Модель", "brand": car.brand.id}),
            content_type='application/json'
        )
        assert r.status_code == 200

        r = self.client.get(f'/api/cars/{car.id}/')
        data = r.json()
        assert data['name'] == "Новая Модель"


    def test_delete_car(self):
        cars = baker.make("Car", 10)  
        r = self.client.get("/api/cars/")
        data = r.json()
        assert len(data) == 10

        car_id_to_delete = cars[3].id
        self.client.delete(f'/api/cars/{car_id_to_delete}/')

        r = self.client.get('/api/cars/')
        data = r.json()
        assert len(data) == 9

        assert car_id_to_delete not in [i['id'] for i in data]
        
#mixin owner
class OwnerViewsetTestCase(TestCase):
    def test_get_list(self):
        owner = baker.make("Owner")
        r = self.client.get("/api/owners/")
        data = r.json()
        assert owner.name == data[0]['name']
        assert owner.id == data[0]['id']
        assert len(data) == 1

    def test_create_owner(self):
        car = baker.make("Car")
        r = self.client.post("/api/owners/", {"name": "Малахов В.С.", "car": car.id})
        new_owner_id = r.json()['id']
        owners = Owner.objects.all()
        assert len(owners) == 1
        new_owner = Owner.objects.get(id=new_owner_id)
        assert new_owner.name == 'Малахов В.С.'
        assert new_owner.car == car

    def test_retrieve_owner(self):
        owner = baker.make("Owner")
        r = self.client.get(f'/api/owners/{owner.id}/')
        assert r.status_code == 200
        assert r.json()['name'] == owner.name

    def test_update_owner(self):
        car = baker.make("Car")
        owners = baker.make("Owner", 10, car=car)
        owner = owners[2]
        r = self.client.put(
            f'/api/owners/{owner.id}/',
            data=json.dumps({"name": "Герасимова В.С.", "car": car.id}),
            content_type='application/json'
        )
        assert r.status_code == 200
        owner.refresh_from_db()
        assert owner.name == "Герасимова В.С."

    def test_delete_owner(self):
        owners = baker.make("Owner", 10)
        owner_id_to_delete = owners[3].id
        self.client.delete(f'/api/owners/{owner_id_to_delete}/')
        r = self.client.get('/api/owners/')
        data = r.json()
        assert len(data) == 9
        assert owner_id_to_delete not in [i['id'] for i in data]

#mixin service
class ServiceViewsetTestCase(TestCase):
    def test_get_list(self):
        service = baker.make("Service")
        r = self.client.get("/api/services/")
        data = r.json()
        assert service.name == data[0]['name']
        assert service.id == data[0]['id']
        assert len(data) == 1

    def test_create_service(self):
        r = self.client.post("/api/services/", {"name": "Сервис 1", "location": "Москва"})
        new_service_id = r.json()['id']
        services = Service.objects.all()
        assert len(services) == 1
        new_service = Service.objects.get(id=new_service_id)
        assert new_service.name == 'Сервис 1'

    def test_retrieve_service(self):
        service = baker.make("Service")
        r = self.client.get(f'/api/services/{service.id}/')
        assert r.status_code == 200
        assert r.json()['name'] == service.name

    def test_update_service(self):
        services = baker.make("Service", 10)
        service = services[2]
        r = self.client.put(
            f'/api/services/{service.id}/',
            data=json.dumps({"name": "Новый Сервис", "location": "Питер"}),
            content_type='application/json'
        )
        assert r.status_code == 200
        service.refresh_from_db()
        assert service.name == "Новый Сервис"

    def test_delete_service(self):
        services = baker.make("Service", 10)
        service_id_to_delete = services[3].id
        self.client.delete(f'/api/services/{service_id_to_delete}/')
        r = self.client.get('/api/services/')
        data = r.json()
        assert len(data) == 9
        assert service_id_to_delete not in [i['id'] for i in data]        

#mixin servicerecord
class ServiceRecordViewsetTestCase(TestCase):
    def test_get_list(self):
        service_record = baker.make("ServiceRecord")
        r = self.client.get("/api/service-records/")
        data = r.json()
        assert service_record.car.id == data[0]['car']
        assert service_record.service.id == data[0]['service']
        assert len(data) == 1

    def test_create_service_record(self):
        car = baker.make("Car")
        service = baker.make("Service")

        r = self.client.post("/api/service-records/", {
            "car": car.id,
            "service": service.id,
            "date": "2024-01-01",
            "details": "Замена масла"
        }, content_type='application/json')

        new_record = ServiceRecord.objects.get(id=r.json()['id'])
        assert new_record.car == car
        assert new_record.service == service
        assert new_record.details == "Замена масла"

    def test_retrieve_service_record(self):
        service_record = baker.make("ServiceRecord")
        r = self.client.get(f'/api/service-records/{service_record.id}/')
        assert r.status_code == 200
        assert r.json()['details'] == service_record.details

    def test_update_service_record(self):
        service_records = baker.make("ServiceRecord", 10)
        service_record = service_records[2]
        r = self.client.put(
            f'/api/service-records/{service_record.id}/',
            data=json.dumps({
            "car": service_record.car.id,
            "service": service_record.service.id,
            "date": str(service_record.date),
            "details": "Замена фильтра"
        }),
        content_type='application/json'
        )
        assert r.status_code == 200
        service_record.refresh_from_db()
        assert service_record.details == "Замена фильтра"

    def test_delete_service_record(self):
        service_records = baker.make("ServiceRecord", 10)
        service_record_id_to_delete = service_records[3].id
        self.client.delete(f'/api/service-records/{service_record_id_to_delete}/')
        r = self.client.get('/api/service-records/')
        data = r.json()
        assert len(data) == 9
        assert service_record_id_to_delete not in [i['id'] for i in data]