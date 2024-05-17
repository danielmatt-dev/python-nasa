import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from users.schema import UserType
from .models import ImageNasa, Vote

class ImageNasaType(DjangoObjectType):
    class Meta:
        model = ImageNasa

class Query(graphene.ObjectType):
    all_images = graphene.List(ImageNasaType)

    def resolve_all_images(self, info, **kwargs):
        return ImageNasa.objects.all()

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    all_images = graphene.List(ImageNasaType)
    all_votes = graphene.List(VoteType)

    def resolve_all_images(self, info, **kwargs):
        return ImageNasa.objects.all()

    def resolve_all_votes(self, info, **kwargs):
        return Vote.objects.all()

class CreateImage(graphene.Mutation):
    id = graphene.Int()
    img_url = graphene.String()
    rover_name = graphene.String()
    camera_name = graphene.String()
    earth_date = graphene.Date()
    posted_by = graphene.Field(UserType)

    class Arguments:
        img_src = graphene.String(required=True)
        rover_name = graphene.String(required=True)
        camera_name = graphene.String(required=True)
        earth_date = graphene.Date(required=True)

    def mutate(self, info, img_src, rover_name, camera_name, earth_date):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in to create an image.')

        img = ImageNasa(
            img_src=img_src,
            rover_name=rover_name,
            camera_name=camera_name,
            earth_date=earth_date,
            posted_by=user
        )
        img.save()

        return CreateImage(
            id=img.id,
            img_url=img.img_src,
            rover_name=img.rover_name,
            camera_name=img.camera_name,
            earth_date=img.earth_date,
            posted_by=img.posted_by
        )

class Mutation(graphene.ObjectType):
    create_image = CreateImage.Field()

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    img = graphene.Field(ImageNasaType)

    class Arguments:
        img_id = graphene.Int()

    def mutate(self, info, img_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        img = ImageNasa.objects.filter(id=img_id).first()
        if not img:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            imageNasa=img
        )

        return CreateVote(user=user, img=img)

class Mutation(graphene.ObjectType):
    create_image = CreateImage.Field()
    create_vote = CreateVote.Field()
