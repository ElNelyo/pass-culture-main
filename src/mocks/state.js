import offerTypes from './api/offer_types'

const state = {
  data: {
    bookings: [
      {
        id: 'A9',
        amount: 10,
        dateCreated: '2018-10-29T09:44:39.143513Z',
        isCancelled: false,
        isUsed: false,
        modelName: 'Booking',
        quantity: 1,
        qrCode: 'data:image/png;base64,iVIVhzdjeizfjezfoizejojczez',
        recommendationId: null,
        stock: {
          available: 10,
          bookingLimitDatetime: '2018-11-27T23:59:56.790000Z',
          bookingRecapSent: null,
          dateModified: '2018-10-29T09:44:38.649450Z',
          dateModifiedAtLastProvider: '2018-10-29T09:44:38.649416Z',
          beginningDatetime: '2018-11-30T21:42:56.790000Z',
          endDatetime: '2018-11-30T22:42:56.790000Z',
          groupSize: 1,
          id: 'AE',
          idAtProviders: null,
          isSoftDeleted: false,
          lastProviderId: null,
          modelName: 'Stock',
          offerId: null,
          price: 10,
          resolvedOffer: {
            bookingEmail: null,
            dateCreated: '2018-10-29T09:44:38.216817Z',
            dateModifiedAtLastProvider: '2018-10-29T09:44:38.216792Z',
            productId: 'AE',
            product: {
              accessibility: '\u0000',
              ageMax: null,
              ageMin: null,
              conditions: null,
              dateModifiedAtLastProvider: '2018-10-29T09:44:38.012002Z',
              description: null,
              durationMinutes: 60,
              extraData: null,
              id: 'AE',
              idAtProviders: null,
              isNational: false,
              lastProviderId: null,
              mediaUrls: [],
              modelName: 'Product',
              name: 'Rencontre avec Franck Lepage',
              thumbCount: 1,
              type: 'EventType.CONFERENCE_DEBAT_DEDICACE',
            },
            id: 'AM3A',
            idAtProviders: null,
            isActive: true,
            lastProviderId: null,
            modelName: 'Offer',
            venue: {
              address: '1 BD POISSONNIERE',
              bic: null,
              bookingEmail: 'fake@email.com',
              city: 'Paris',
              comment: null,
              dateModifiedAtLastProvider: '2018-10-29T09:44:37.451422Z',
              departementCode: '75',
              iban: null,
              id: 'AE',
              idAtProviders: null,
              isVirtual: false,
              lastProviderId: null,
              latitude: 48.87067,
              longitude: 2.3478,
              managingOffererId: 'AE',
              modelName: 'Venue',
              name: 'LE GRAND REX PARIS',
              postalCode: '75002',
              siret: '50763357600016',
              thumbCount: 0,
            },
            venueId: 'AE',
          },
        },
        stockId: 'AE',
        token: '2AEVY3',
        userId: 'AE',
      },
    ],
    favorites: [{ id: 'D4', offerId: 'AM3A' }],
    features: [
      {
        id: 'E5',
        isActive: true,
        nameKey: 'QR_CODE',
      },
    ],
    mediations: [{ id: 'B4', offerId: 'AM3A' }],
    offers: [
      {
        bookingEmail: null,
        dateCreated: '2018-10-29T09:44:38.329923Z',
        dateModifiedAtLastProvider: '2018-10-29T09:44:38.329902Z',
        dateRange: [],
        productId: 'AM',
        product: {
          accessibility: '\u0000',
          ageMax: null,
          ageMin: null,
          conditions: null,
          dateModifiedAtLastProvider: '2018-10-29T09:44:38.095898Z',
          description: null,
          durationMinutes: 10,
          extraData: null,
          id: 'AM',
          idAtProviders: null,
          isNational: false,
          lastProviderId: null,
          mediaUrls: [],
          modelName: 'Product',
          name: 'PNL chante Marx',
          thumbCount: 1,
          type: 'EventType.MUSIQUE',
        },
        id: 'AM3A',
        idAtProviders: null,
        isActive: true,
        lastProviderId: null,
        name: 'super offre',
        type: 'EventType.SPECTACLE_VIVANT',
        modelName: 'Offer',
        stocks: [],
        venue: {
          address: '6 rue Grolee',
          bic: null,
          bookingEmail: 'fake2@email.com',
          city: 'Lyon',
          comment: null,
          dateModifiedAtLastProvider: '2018-10-29T09:44:37.714362Z',
          departementCode: '69',
          iban: null,
          id: 'AM',
          idAtProviders: null,
          isVirtual: false,
          lastProviderId: null,
          latitude: 45.76261,
          longitude: 4.83669,
          managingOfferer: {
            address: '6 RUE GROLEE',
            bic: null,
            city: 'Lyon',
            dateCreated: '2018-10-29T09:44:16.333150Z',
            dateModifiedAtLastProvider: '2018-10-29T09:44:16.333119Z',
            iban: null,
            id: 'A9',
            idAtProviders: null,
            isActive: true,
            lastProviderId: null,
            modelName: 'Offerer',
            name: 'THEATRE DE L ODEON',
            postalCode: '69002',
            siren: '750505703',
            thumbCount: 0,
          },
          managingOffererId: 'A9',
          modelName: 'Venue',
          name: 'THEATRE DE L ODEON',
          postalCode: '69002',
          siret: '75050570300025',
          thumbCount: 0,
        },
        venueId: 'AM',
      },
    ],
    recommendations: [
      {
        id: 'AM',
        dateCreated: '2018-10-29T09:49:07.372801Z',
        dateRead: null,
        dateUpdated: '2018-10-29T09:49:07.372820Z',
        isClicked: true,
        isFavorite: false,
        isFirst: false,
        mediationId: 'B4',
        modelName: 'Recommendation',
        offer: {
          bookingEmail: null,
          dateCreated: '2018-10-29T09:44:38.216817Z',
          dateModifiedAtLastProvider: '2018-10-29T09:44:38.216792Z',
          dateRange: ['2018-10-29T21:42:56.790000Z', '2018-12-28T22:42:56.790000Z'],
          productId: 'AE',
          product: {
            accessibility: '\u0000',
            ageMax: null,
            ageMin: null,
            conditions: null,
            dateModifiedAtLastProvider: '2018-10-29T09:44:38.012002Z',
            description: null,
            durationMinutes: 60,
            extraData: null,
            id: 'AE',
            idAtProviders: null,
            isNational: false,
            lastProviderId: null,
            mediaUrls: [],
            modelName: 'Product',
            name: 'Rencontre avec Franck Lepage',
            thumbCount: 1,
            type: 'EventType.CONFERENCE_DEBAT_DEDICACE',
          },
          id: 'AE',
          idAtProviders: null,
          isActive: true,
          lastProviderId: null,
          modelName: 'Offer',
          stocks: [
            {
              available: 10,
              bookingLimitDatetime: '2018-11-27T23:59:56.790000Z',
              bookingRecapSent: null,
              dateModified: '2018-10-29T09:44:38.649450Z',
              dateModifiedAtLastProvider: '2018-10-29T09:44:38.649416Z',
              beginningDatetime: '2018-11-30T21:42:56.790000Z',
              endDatetime: '2018-11-30T22:42:56.790000Z',
              groupSize: 1,
              id: 'AE',
              idAtProviders: null,
              isSoftDeleted: false,
              lastProviderId: null,
              modelName: 'Stock',
              offerId: null,
              price: 10,
            },
            {
              available: 15,
              bookingLimitDatetime: '2018-10-26T23:59:56.790000Z',
              bookingRecapSent: null,
              dateModified: '2018-10-29T09:44:38.709256Z',
              dateModifiedAtLastProvider: '2018-10-29T09:44:38.709232Z',
              beginningDatetime: '2018-10-29T21:42:56.790000Z',
              endDatetime: '2018-10-29T22:42:56.790000Z',
              groupSize: 1,
              id: 'A9',
              idAtProviders: null,
              isSoftDeleted: false,
              lastProviderId: null,
              modelName: 'Stock',
              offerId: null,
              price: 15,
            },
            {
              available: 100,
              bookingLimitDatetime: '2018-12-25T23:59:56.790000Z',
              bookingRecapSent: null,
              dateModified: '2018-10-29T09:44:38.752035Z',
              dateModifiedAtLastProvider: '2018-10-29T09:44:38.752013Z',
              beginningDatetime: '2018-12-28T21:42:56.790000Z',
              endDatetime: '2018-12-28T22:42:56.790000Z',
              groupSize: 1,
              id: 'AM',
              idAtProviders: null,
              isSoftDeleted: false,
              lastProviderId: null,
              modelName: 'Stock',
              offerId: null,
              price: 10,
            },
            {
              available: 100,
              bookingLimitDatetime: '2018-12-24T23:59:56.790000Z',
              bookingRecapSent: null,
              dateModified: '2018-10-29T09:44:38.808864Z',
              dateModifiedAtLastProvider: '2018-10-29T09:44:38.808845Z',
              beginningDatetime: '2018-12-27T21:42:56.790000Z',
              endDatetime: '2018-12-27T22:42:56.790000Z',
              groupSize: 1,
              id: 'AQ',
              idAtProviders: null,
              isSoftDeleted: false,
              lastProviderId: null,
              modelName: 'Stock',
              offerId: null,
              price: 10,
            },
            {
              available: 90,
              bookingLimitDatetime: '2018-12-23T23:59:56.790000Z',
              bookingRecapSent: null,
              dateModified: '2018-10-29T09:44:38.848728Z',
              dateModifiedAtLastProvider: '2018-10-29T09:44:38.848696Z',
              beginningDatetime: '2018-12-26T21:42:56.790000Z',
              endDatetime: '2018-12-26T22:42:56.790000Z',
              groupSize: 1,
              id: 'AU',
              idAtProviders: null,
              isSoftDeleted: false,
              lastProviderId: null,
              modelName: 'Stock',
              offerId: null,
              price: 15,
            },
          ],
          venue: {
            address: '1 BD POISSONNIERE',
            bic: null,
            bookingEmail: 'fake@email.com',
            city: 'Paris',
            comment: null,
            dateModifiedAtLastProvider: '2018-10-29T09:44:37.451422Z',
            departementCode: '75',
            iban: null,
            id: 'AE',
            idAtProviders: null,
            isVirtual: false,
            lastProviderId: null,
            latitude: 48.87067,
            longitude: 2.3478,
            managingOfferer: {
              address: '1 BD POISSONNIERE',
              bic: null,
              city: 'Paris',
              dateCreated: '2018-10-29T09:44:16.271422Z',
              dateModifiedAtLastProvider: '2018-10-29T09:44:16.271380Z',
              iban: null,
              id: 'AE',
              idAtProviders: null,
              isActive: true,
              lastProviderId: null,
              modelName: 'Offerer',
              name: 'LE GRAND REX PARIS',
              postalCode: '75002',
              siren: '507633576',
              thumbCount: 0,
            },
            managingOffererId: 'AE',
            modelName: 'Venue',
            name: 'LE GRAND REX PARIS',
            postalCode: '75002',
            siret: '50763357600016',
            thumbCount: 0,
          },
          venueId: 'AE',
        },
        offerId: 'AE',
        search: null,
        shareMedium: null,
        userId: 'AE',
        bookingsIds: ['A9', 'AE', 'AM', 'AQ', 'AY', 'AU', 'A4'],
      },
    ],
    stocks: [
      {
        available: 10,
        bookingLimitDatetime: '2018-11-27T23:59:56.790000Z',
        bookingRecapSent: null,
        dateModified: '2018-10-29T09:44:38.649450Z',
        dateModifiedAtLastProvider: '2018-10-29T09:44:38.649416Z',
        beginningDatetime: '2018-11-30T21:42:56.790000Z',
        endDatetime: '2018-11-30T22:42:56.790000Z',
        groupSize: 1,
        id: 'AE',
        idAtProviders: null,
        isSoftDeleted: false,
        lastProviderId: null,
        modelName: 'Stock',
        offerId: 'AM3A',
        price: 10,
        resolvedOffer: {
          bookingEmail: null,
          dateCreated: '2018-10-29T09:44:38.216817Z',
          dateModifiedAtLastProvider: '2018-10-29T09:44:38.216792Z',
          productId: 'AE',
          product: {
            accessibility: '\u0000',
            ageMax: null,
            ageMin: null,
            conditions: null,
            dateModifiedAtLastProvider: '2018-10-29T09:44:38.012002Z',
            description: null,
            durationMinutes: 60,
            extraData: null,
            id: 'AE',
            idAtProviders: null,
            isNational: false,
            lastProviderId: null,
            mediaUrls: [],
            modelName: 'Product',
            name: 'Rencontre avec Franck Lepage',
            thumbCount: 1,
            type: 'EventType.CONFERENCE_DEBAT_DEDICACE',
          },
          id: 'AE',
          idAtProviders: null,
          isActive: true,
          lastProviderId: null,
          modelName: 'Offer',
          venue: {
            address: '1 BD POISSONNIERE',
            bic: null,
            bookingEmail: 'fake@email.com',
            city: 'Paris',
            comment: null,
            dateModifiedAtLastProvider: '2018-10-29T09:44:37.451422Z',
            departementCode: '75',
            iban: null,
            id: 'AE',
            idAtProviders: null,
            isVirtual: false,
            lastProviderId: null,
            latitude: 48.87067,
            longitude: 2.3478,
            managingOffererId: 'AE',
            modelName: 'Venue',
            name: 'LE GRAND REX PARIS',
            postalCode: '75002',
            siret: '50763357600016',
            thumbCount: 0,
          },
          venueId: 'AE',
        },
      },
    ],
    types: offerTypes,
    users: [
      {
        id: 'AE',
        canBookFreeOffers: true,
        dateCreated: '2018-10-29T09:44:18.243300Z',
        departementCode: '93',
        email: 'pctest.jeune.93@btmx.fr',
        expenses: {
          all: {
            actual: 230,
            max: 500,
          },
          digital: {
            actual: 0,
            max: 200,
          },
          physical: {
            actual: 0,
            max: 100,
          },
        },
        firstName: 'PC Test',
        isAdmin: false,
        lastName: 'Jeune 93',
        modelName: 'User',
        phoneNumber: null,
        postalCode: '93100',
        publicName: 'PC Test Jeune 93',
        thumbCount: 1,
        wallet_balance: 270,
        wallet_is_activated: true,
      },
    ],
  },
  errors: {},
  form: {},
  geolocation: {
    latitude: 48.8637404,
    longitude: 2.3374129,
    watchId: 1,
  },
  loading: {
    config: {},
    isActive: false,
  },
  menu: false,
  modal: {
    config: {
      fromDirection: 'right',
    },
    isActive: false,
    $modal: null,
  },
  share: {
    options: false,
    visible: false,
  },
  splash: {
    closeTimeout: 1000,
    isActive: false,
  },
  user: {
    id: 'AE',
    canBookFreeOffers: true,
    dateCreated: '2018-10-29T09:44:18.243300Z',
    departementCode: '93',
    email: 'pctest.jeune.93@btmx.fr',
    expenses: {
      all: {
        actual: 230,
        max: 500,
      },
      digital: {
        actual: 0,
        max: 200,
      },
      physical: {
        actual: 0,
        max: 100,
      },
    },
    firstName: 'PC Test',
    isAdmin: false,
    lastName: 'Jeune 93',
    modelName: 'User',
    phoneNumber: null,
    postalCode: '93100',
    publicName: 'PC Test Jeune 93',
    thumbCount: 1,
    wallet_balance: 270,
    wallet_is_activated: true,
  },
  card: {
    draggable: true,
    isActive: false,
    areDetailsVisible: false,
    unFlippable: false,
  },
  _persist: {
    version: -1,
    rehydrated: true,
  },
}

export default state
