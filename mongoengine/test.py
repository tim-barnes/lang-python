import mongoengine


class Organization(mongoengine.Document):
    name = mongoengine.StringField(required=True)


class User(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    uid = mongoengine.IntField(required=True)
    password = mongoengine.StringField(required=True)
    public_name = mongoengine.StringField(required=True)
    organization = mongoengine.ReferenceField(Organization, required=True, reverse_delete_rule=mongoengine.CASCADE)

    meta = {'allow_inheritance': True}


mongoengine.connect(host='mongodb://localhost/logins')
User.drop_collection()
Organization.drop_collection()



trueai = Organization(name='trueai')
trueai.save()

gabriela = User(name='gabriela',
                uid='1',
                password='gabriela',
                public_name='Gabriela M',
                organization=trueai)
gabriela.save()

tim = User(name='tim',
           uid='2',
           password='goo',
           public_name='Tim B',
           organization=trueai)
tim.save()


# Iterate Users
for u in User.objects:
    print(u.name, " ", u.id)

# find a user
print(User.objects(name="tim"))

