import {
  GetIndividualOfferResponseModel,
  OfferStatus,
  SubcategoryIdEnum,
} from 'apiClient/v1'
import { IndividualOffer } from 'core/Offers/types'
import { GetIndividualOfferFactory } from 'utils/apiFactories'

import {
  serializeOfferApiImage,
  serializeOfferApiExtraData,
  serializeOfferApi,
} from '../serializers'

describe('serializer', () => {
  const serializeOfferApiImageDataSet = [
    {
      activeMediation: {
        thumbUrl: 'https://image.url',
        credit: 'John Do',
      } as unknown as GetIndividualOfferResponseModel[],
      expectedImage: {
        originalUrl: 'https://image.url',
        url: 'https://image.url',
        credit: 'John Do',
      },
    },
    {
      activeMediation: {} as unknown as GetIndividualOfferResponseModel[],
      expectedImage: undefined,
    },
    {
      activeMediation: {
        credit: 'John Do',
      } as unknown as GetIndividualOfferResponseModel[],
      expectedImage: undefined,
    },
    {
      activeMediation: {
        thumbUrl: 'https://image.url',
        credit: null,
      } as unknown as GetIndividualOfferResponseModel[],
      expectedImage: {
        originalUrl: 'https://image.url',
        url: 'https://image.url',
        credit: '',
      },
    },
  ]
  it.each(serializeOfferApiImageDataSet)(
    'serializeOfferApiImage from mediation',
    ({ activeMediation, expectedImage }) => {
      const offerApi = {
        activeMediation,
      } as unknown as GetIndividualOfferResponseModel

      expect(serializeOfferApiImage(offerApi)).toEqual(expectedImage)
    }
  )

  it('serializeOfferApiImage from thumbUrl', () => {
    const offerApi = {
      thumbUrl: 'https://image.url',
      mediations: [],
    } as unknown as GetIndividualOfferResponseModel

    expect(serializeOfferApiImage(offerApi)).toEqual({
      originalUrl: 'https://image.url',
      url: 'https://image.url',
      credit: '',
    })
  })

  it('serializeOfferApiExtraData', () => {
    const offerApi = {
      extraData: {
        author: 'test author',
        gtl_id: '07000000',
        performer: 'test performer',
        ean: 'test ean',
        showType: 'test showType',
        showSubType: 'test showSubType',
        speaker: 'test speaker',
        stageDirector: 'test stageDirector',
        visa: 'test visa',
      },
    } as unknown as GetIndividualOfferResponseModel

    expect(serializeOfferApiExtraData(offerApi)).toEqual({
      author: 'test author',
      gtl_id: '07000000',
      performer: 'test performer',
      ean: 'test ean',
      showType: 'test showType',
      showSubType: 'test showSubType',
      speaker: 'test speaker',
      stageDirector: 'test stageDirector',
      visa: 'test visa',
    })
  })

  it('serializeOfferApi', () => {
    const offerApi: GetIndividualOfferResponseModel = GetIndividualOfferFactory(
      { bookingsCount: 123 }
    )
    const offerSerialized: IndividualOffer = {
      audioDisabilityCompliant: true,
      visualDisabilityCompliant: true,
      mentalDisabilityCompliant: true,
      motorDisabilityCompliant: true,
      author: '',
      bookingsCount: 123,
      dateCreated: '2020-04-12T19:31:12Z',
      ean: '',
      image: undefined,
      hasBookingLimitDatetimesPassed: false,
      hasStocks: true,
      isActive: true,
      isActivable: true,
      isDigital: false,
      isDuo: true,
      isEditable: true,
      isEvent: true,
      isNational: true,
      isNonFreeOffer: true,
      isThing: true,
      lastProvider: null,
      gtl_id: '',
      name: 'Le nom de l’offre 1',
      id: 1,
      performer: '',
      priceCategories: [
        {
          id: 1,
          label: 'mon label',
          price: 66.6,
        },
      ],
      showSubType: '',
      showType: '',
      speaker: '',
      stageDirector: '',
      status: OfferStatus.ACTIVE,
      subcategoryId: SubcategoryIdEnum.SEANCE_CINE,
      venue: {
        id: 1,
        audioDisabilityCompliant: true,
        mentalDisabilityCompliant: true,
        motorDisabilityCompliant: true,
        visualDisabilityCompliant: true,
        address: 'Ma Rue',
        city: 'Ma Ville',
        departementCode: '78',
        isVirtual: false,
        name: 'Le nom du lieu 1',
        managingOfferer: {
          name: 'Le nom de la structure 1',
          id: 3,
        },
        postalCode: '11100',
        publicName: 'Mon Lieu',
      },
      visa: '',
    }

    expect(serializeOfferApi(offerApi)).toEqual(offerSerialized)
  })
})
