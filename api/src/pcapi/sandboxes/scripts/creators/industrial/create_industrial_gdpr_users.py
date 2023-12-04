import datetime
import itertools
import logging
import typing
from unicodedata import normalize

from dateutil.relativedelta import relativedelta

from pcapi.core.fraud import factories as fraud_factories
from pcapi.core.fraud import models as fraud_models
from pcapi.core.geography import factories as geography_factories
from pcapi.core.geography.repository import get_iris_from_coordinates
from pcapi.core.history import factories as history_factories
from pcapi.core.offerers import factories as offerers_factories
from pcapi.core.users import factories as users_factories
from pcapi.core.users import models as users_models


logger = logging.getLogger(__name__)


THREE_YEARS_AGO = datetime.datetime.utcnow() - relativedelta(years=3)

INCREMENT = itertools.count()


def _create_email(text: str) -> str:
    slugified = normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8").strip().lower().replace(" ", "-")
    return f"{slugified}@test-rgpd.fr"


def _create_gdpr_user(
    factory: typing.Type, first_name: str, last_connection_date: datetime.datetime, comment: str, **kwargs: typing.Any
) -> users_models.User:
    increment = next(INCREMENT)

    data = {
        "firstName": first_name,
        "lastName": "TEST-RGPD",
        "email": _create_email(first_name),
        "address": "Avenue du Soldat Inconnu",
        "postalCode": "55100",
        "city": "Verdun",
        "departementCode": "55",
        "phoneNumber": f"+33699{increment:06}",
        "dateCreated": THREE_YEARS_AGO - relativedelta(months=6, days=10),
        "lastConnectionDate": last_connection_date,
    }

    data.update(kwargs)
    user = factory(**data)

    history_factories.ActionHistoryFactory(
        authorUser=None,
        user=user,
        comment=f"Créé pour les tests d'anonymisation RGPD\n{comment}",
    )

    return user


def create_industrial_gdpr_users() -> None:
    logger.info("create_industrial_gdpr_users")

    iris_for_default_address = geography_factories.IrisFranceFactory(
        # lat=49.157797, lon=5.378479
        code="555450103",
        shape="0103000020E610000001000000390000003DD93492858B15402F71CC430E9448403F503AF6BE891540D9C1811FD6934840F790A1B331871540F5BE096799934840E837D515BF861540723EEAAC94934840F489280E7886154006FFB82A919348405F19681D4286154087C0123B8C9348407C60D7127C85154066B83AC4789348405F028462608515405D6696DA73934840C8A47F184C851540D13D2B836F934840E1F9A4834285154011B3B2F06B9348403A0CF76446851540F2E56ECE6893484046D0E2195F851540D5D873B36193484090337DBE1F85154021C9EB7F5F9348409C8ADA4F18821540E42FEC193C9348403AD58D058C811540A7E6110433934840D1FF43FD3E811540FC34F3DD2B9348404F1E1935178115408DA96055259348409E094253B2801540F5AF489729934840655E42FB5A80154060A92C852D9348402FFB51361C80154021AF2CD430934840581814C1DC7F1540D50D3D3335934840DC183DCAA97F15406F5C975539934840DFA1651F747F1540F4E15EEB3E934840D4E36081457F15402CED251B45934840996C9A6C157F15409103C02E4D9348409A352689D17E1540CC4CA81459934840F81346028A7E15403F82ABD765934840C18D2564627C1540E99B2D68C89348409266A0C2C97C1540E26E892DF0934840C358AF79DE7C15404A8201C0F293484071965E85927D1540036F774E00944840F87D1863DB7D15409688D6E60494484078CBD1361C7E1540F639312908944840BA0ED46DC17F1540ADBCFD8F149448403B7EC419AC811540CB2FBE391D944840D20C3FC318831540A51CBAAA3C944840977D69BE1A841540BB4D9CAE5E9448401742A669EE831540CEEC17EC7294484050BF0615F983154086E5F72487944840AEBAEB60FE8315407FB1C2B48E944840D8EE0BA90B8415401A97DA6D98944840D63CFBA51D841540F1C29D48A0944840E1F5E590B387154008A93ACDB6944840ABF22351EA871540E57C2D0DB89448402B23A9A6DE8815404F1C297DBD944840FB1FBC316F8915404ADCA175BF944840B276144F868A15402D8CB2E0BA944840CD531B9E288C154093B19B49BC944840774544535E8C154086F5CBA7BC944840CD816321618C1540B4053FB7B2944840D5BFDABD518C154053D2C102AF94484031E55D494A8C15409B1BDC51AD94484002E088F6188C154052D43464A3944840DB042F13918B15408C87001D89944840A9654E9DEB8A1540989F8580719448404E95C3DF338B154032DC73D43C9448403DD93492858B15402F71CC430E944840",
    )

    _create_gdpr_user(
        users_factories.NonAttachedProFactory,
        "Pro non rattaché",
        THREE_YEARS_AGO - relativedelta(months=1),
        "Compte pro non rattaché, dernière connexion il y a plus de 3 ans",
    )

    _create_gdpr_user(
        users_factories.ProFactory,
        "Pro rattaché",
        THREE_YEARS_AGO - relativedelta(months=1),
        "Compte pro avec rattachement validé, dernière connexion il y a plus de 3 ans",
    )

    _create_gdpr_user(
        users_factories.BeneficiaryGrant18Factory,
        "Jeune bénéficiaire",
        THREE_YEARS_AGO - relativedelta(months=1),
        "Jeune bénéficiaire, dernière connexion il y a plus de 3 ans",
        dateOfBirth=THREE_YEARS_AGO - relativedelta(years=19, months=3),
        validatedBirthDate=THREE_YEARS_AGO - relativedelta(years=19, months=3),
        civility="M.",
        activity="Étudiant",
        deposit__source="sandbox",
        deposit__dateCreated=THREE_YEARS_AGO - relativedelta(years=19, months=3) + relativedelta(years=18),
        deposit__expirationDate=THREE_YEARS_AGO - relativedelta(years=19, months=3) + relativedelta(years=18 + 2),
    )

    _create_gdpr_user(
        users_factories.AdminFactory,
        "Ancien interne admin",
        THREE_YEARS_AGO - relativedelta(months=1),
        "Ancien interne admin, dernière connexion il y a plus de 3 ans",
        isActive=False,
    )

    _create_gdpr_user(
        users_factories.UserFactory,
        "Ancien interne non admin",
        THREE_YEARS_AGO - relativedelta(months=1),
        "Ancien interne non admin, dernière connexion il y a plus de 3 ans",
        isActive=False,
    )

    _create_gdpr_user(
        users_factories.UserFactory,
        "Connecté Moins de 3 ans",
        THREE_YEARS_AGO + relativedelta(months=1),
        "Utilisateur grand public, dernière connexion il y a moins de 3 ans",
    )

    _create_gdpr_user(
        users_factories.UserFactory,
        "Connecté Pile 3 ans demain",
        THREE_YEARS_AGO + relativedelta(days=1),
        "Utilisateur grand public, dernière connexion il y pile 3 ans demain",
    )

    user = _create_gdpr_user(
        users_factories.UserFactory,
        "Connecté Pile 3 ans hier",
        THREE_YEARS_AGO - relativedelta(days=1),
        "Utilisateur grand public avec fraud checks, dernière connexion il y pile 3 ans hier",
        dateOfBirth=THREE_YEARS_AGO - relativedelta(years=18, months=2),
        civility="Mme",
        activity="Lycéen",
    )
    fraud_factories.BeneficiaryFraudCheckFactory(user=user)
    fraud_factories.BeneficiaryFraudReviewFactory(user=user, review=fraud_models.FraudReviewStatus.KO)

    _create_gdpr_user(
        users_factories.UserFactory,
        "Connecté Pile 3 ans hier avec Iris",
        THREE_YEARS_AGO - relativedelta(days=1),
        "Utilisateur grand public avec Iris, dernière connexion il y pile 3 ans hier",
        civility="M.",
        activity="Employé",
        # Location is not consistent with address but it must match Iris data created in sandbox
        irisFrance=get_iris_from_coordinates(lat=17.900710, lon=-62.834786),
    )

    user = _create_gdpr_user(
        users_factories.UserFactory,
        "Connecté Pile 3 ans aujourd'hui",
        THREE_YEARS_AGO,
        "Utilisateur grand public avec fraud checks, dernière connexion il y pile 3 ans aujourd'hui",
        dateOfBirth=THREE_YEARS_AGO - relativedelta(years=18, months=3),
        civility="M.",
        activity="Apprenti",
    )
    fraud_factories.BeneficiaryFraudCheckFactory(user=user)
    fraud_factories.BeneficiaryFraudReviewFactory(user=user, review=fraud_models.FraudReviewStatus.KO)

    _create_gdpr_user(
        users_factories.UserFactory,
        "Connecté Pile 3 ans aujourd'hui avec Iris",
        THREE_YEARS_AGO,
        "Utilisateur grand public avec Iris, dernière connexion il y pile 3 ans aujourd'hui",
        # Location is not consistent with address but it must match Iris data created in sandbox
        irisFrance=get_iris_from_coordinates(lat=17.900710, lon=-62.834786),
    )

    user = _create_gdpr_user(
        users_factories.UserFactory,
        "Connecté Plus de 3 ans Ville",
        THREE_YEARS_AGO - relativedelta(months=6),
        "Garçon en ville, dernière connexion il y plus de 3 ans",
        dateOfBirth=THREE_YEARS_AGO - relativedelta(years=18, months=9),
        civility="M.",
        activity="Alternant",
        address="1w Place Charles de Gaulle",
        postalCode="75016",
        city="Paris",
        irisFrance=geography_factories.IrisFranceFactory(
            # lat=48.873437, lon=2.294899
            code="751166409",
            shape="0103000020E61000000100000018000000E19D8D6D3B4C0240D0813AFFAC6F48406851A75C8B4C0240D1D5A38EAD6F484031F20C1B365102402C7B59E2B56F48405001CF8F6A55024068EDFE7EC16F4840860708E66C5A0240B4D32F48DA6F4840BF96CF099F5A02408EC99266E06F484079FB056D185B0240F7A268B4DD6F48408228FE26F95B0240960F9B21D96F4840EC4B07C6395C02403422A9CCD76F4840B2B19016705C024046495E8CD46F48403BE6F795455D02409D979E65C86F4840D770E093055D0240284761E6C66F484003E611E8B75C0240CE70EDC7C56F4840A4009F1B6A5C0240BFA05840C56F48409EE302EC125C02404AD20A29C56F4840906CC6DD445A024010DEAC25AC6F484071C3ADE3C456024038EFE4CF5E6F4840B7B996D9245502403BC252E93A6F484023A1AFB3D6540240F6EF8F4D3F6F4840CB4B1862085302406527A7B4556F4840D685B84952520240B3F319C65E6F48409223CB77A44F02407A1D052D816F484020B65394864C0240CAA64448A96F4840E19D8D6D3B4C0240D0813AFFAC6F4840",
        ),
    )
    fraud_factories.BeneficiaryFraudCheckFactory(user=user)
    fraud_factories.BeneficiaryFraudReviewFactory(user=user, review=fraud_models.FraudReviewStatus.KO)

    user = _create_gdpr_user(
        users_factories.UserFactory,
        "Connecté Plus de 3 ans Campagne",
        THREE_YEARS_AGO - relativedelta(months=6),
        "Fille à la campagne, dernière connexion il y plus de 3 ans",
        dateOfBirth=THREE_YEARS_AGO - relativedelta(years=18, months=8),
        civility="Mme",
        activity="Volontaire en service civique rémunéré",
        address="15 L'Ortille",
        postalCode="60200",
        city="Compiègne",
        irisFrance=geography_factories.IrisFranceFactory(
            # lat=49.49421, lon=2.811936
            code="601591901",
            shape="0103000020E610000001000000F30000002FE22DAFA9B906404952711E4CB24840C484C61006C206407BBA1B2434B24840D0B87228CBCA0640A43724481AB248406AB0C24DA5D006409641CDC808B248403AB8BD9C1DD706408246BE52F5B14840E47ED075ADDB0640DB3EDF3E3CB24840A75AA6893AE1064014E77E7B9AB248400C5D589A6DE606407BC72CB5F6B248403A3FAC55C7E90640BA6205A32BB3484038D1227611E506407C5CECA93CB348406CEBE8272FDB0640FA4E4D1E60B34840A29D0450F2D40640C7E3A65A76B348405E870701C2CF06403E2A5B569DB3484007ADBE6102CF0640CCBFB9F2A2B34840492AF1B055C806402D282AC4D3B34840D775667CC6C4064019F0BDF7EEB34840EE8B0A59C9C4064050460F87EFB3484035DB0C483ECB0640618F82B1E9B34840A0931373A2D406403D5AA051DFB34840B1CFC05879D606401266051EDEB348401DD0A3F6E9D606407C92D7FADEB348400B877C4653D706409CD089B2E1B348409808B221B8D70640D52F5D27E7B34840BED5F90785D90640CEF700D103B448402685FD312EDF0640F8C47E6D5BB4484065442A182FE10640C5FBD79079B4484046962D26DDE20640354C863893B448408CC4897BAEE40640E8FCB5C3AFB44840D667C7AFD9E4064034DF1CCDB2B448405B5E7DAE42E506408569525ABDB44840FD6AF29978E506401167AB28C3B44840E6A4EA0026E406406C0A1BA724B548408612F48405E30640916016EF7EB548401E2884A437E206409740F1E4C1B5484082507B3309E20640ED4B29C0C6B548401E7D59A5D8E1064087ABAA5ECAB54840ED975B8E87E10640DB5672A2CEB548403566F10A30E1064006CE2C1AD1B54840AFB2A84B4CE00640E5AB3FBDD5B548404088B15D6BD30640C990262C16B648400AEFE1EC63CA0640AD36807511B64840D1A80F7EFAC90640B85A5BAF10B648401056E2D9D4C90640348A16AD21B64840610A66F8F9CD0640AFB4333552B648401FCBC8D61ED20640D38EB38A89B6484099A98128F1D60640737F891FC1B64840B8CEFF938AD8064010236E03C6B64840EB71F65314DA0640045CC2ECC5B64840BAD7617879DD0640114E36AAC5B6484008D53A6C79DE064043FDDF25C1B6484068F5731CBEDE064042F9BD73AFB64840208D365C99E10640A5080F119CB64840850CD7201EE30640CE46E6009AB64840B589D08DF3EC0640C3BABBDCB2B64840CB484AE4C9F50640DF37C607BDB64840664FDAD490FC064058644BC3C7B64840293658CC1C050740A49497D5D7B648409900E960E70807402CE447A1D9B64840F1AEF46B720D07400AFCF0E1CDB64840AA51861F660F07402FA8AFECC0B648403B67C4214D120740A1416040B8B64840062DD10A26150740080505CCB9B64840BC1807D1F1180740C96E52B0CCB648402CADC80C501C0740859EFC65DCB64840D6911AACA51F074049D36C5CE2B64840CD9FC9CC0C240740A9CA9D29CDB64840841F0733DE24074014A6EE0DA3B648401B317EEDED24074011D4024C92B64840505248CCBF260740995056A67FB64840F4E6C0AF8F2B0740A5DE41C44EB648408EBFEC3E972C07402515FE2369B64840507A8B4465300740533F8AE6D5B648404D31D2AAA531074092EDD91CF9B648405B1BCAB855330740F2E92B7E27B748408D8AE55AFF370740D03DEE9D55B74840F9742EAE44380740857E7EDB56B74840DA28834F183F0740776F446D75B748404DB4AE219946074016F7E57A84B748403F50E76EFF4907406C3582C477B74840F50F6D9AC94C0740F233EF9A5FB74840B87A5F9DF84D0740F045A33F48B74840C6C9B371354E07408095F52743B748405C1E2E75524E0740F5B8A5F93EB74840F8435F09594E07407A13E8253CB748407D1F16D2D74D0740D86199281DB7484082694D035D4D07401AD148D201B7484049D3BAFDEC4F07405365036BB2B64840D8BA53EC68500740E99F10BAA3B64840CEFDFE5D30530740714D38A757B64840DA2D5470575507409B20ACFF40B64840B45E13AE4956074034D911F037B64840F18889DEA6580740D364AEE722B64840C96AF4D39E58074078D826A526B64840951C27EB3F580740B7413D7331B64840B26681DF9F570740C3085EE040B6484026D18D691B570740DE1F9F004BB64840EFE0DE329C580740C3F3304C55B6484027463824865907404255B31B5AB648407F881D1589590740533D7C1358B648402DD685D7F35A07403E4B3C1337B6484017CD24EB0D5B0740F2043B4734B64840FE750D8E2E5B07408E40A6272FB6484088B515B8585B07406429C38D24B6484079C0A89A755B0740D5AE840B08B648406F879D60965B0740BF9A7262FDB548401890B1A0B55B0740D20195D8F5B54840848408D1DC5B074000BC329AEEB548403824DF37575C07408E640BB5E1B54840013EEC239F5D07400C5B2FC5C5B5484090AA3B7D945E0740C0DA4E9BB2B54840C097FEC6965F07409A35BCCCA1B548405475EFDFD75F0740DA15163D9EB54840224767F43A6007407511F45299B54840F2B0D54F776707409EBFC3E14EB54840A648A0AA0D68074016D900E949B5484014D1A6D6F7680740CF42389643B54840BB1B0C0E016A07403800FBD23DB5484061C00844F76B0740CB85826334B54840A02B3989836F0740E3DB53B924B548405AFAADB0F17007407B2123E326B54840B93E5550E8700740CC8BB64426B54840637A2183876F074038F77F23D2B44840FCF5D857716F0740D926A510C8B448406E9F5275766F07404F76055BC5B448402884A85B3B6F0740C494CEB2BFB448408537D8F4606E07402BB951CFABB44840672BAF67AC630740E0A53445DAB448406077C26C7863074041626753D9B44840FAE4F9908D6107405F9E14CECDB4484070BADDF5296107403EB3281BCBB44840541C10444A600740B52FFCB3C2B44840C5171F747A5F07401B40FBAEBAB448402FF92E9C505F0740610F74C4B8B44840CF0419963E5F07404466F870B7B448407A1052E0975E07408B906773A3B448400158A56DEF5C07401626F27D6EB448408748A008705C07405815B9DF5CB448405461A8B1645C07400E76522F54B4484048EA73DE885C07403B4DA69051B44840DBC0F620E15C074098DA45714BB4484053E3AFC4C25E07404B66E39930B4484092280FD1075E074088A92321B7B348409616CE7ECF5D07404524C5EBB6B348405F351333C35D0740AF7C38B7B7B34840907709341D5B0740FFEE5736B4B3484007578B06EC530740CFD2E13CAAB34840829E8E1AE852074036F8348CA8B34840CD110A250A510740174A55F489B34840F8B55B37624D07405B28B32257B3484024F5B2E0F64907400A3075AD28B34840A28EB8B095460740D8CCE76CFAB24840EE24399BE84507404E7F4806F3B248406F9C512933410740E9A7F9F8CCB248404E4ECAC233360740CD6016CC74B2484010167BAD6934074006B02F5868B24840E3862CE96C320740C931ABBF60B24840CFC80387AA23074057994E8D26B248406C819734ED1D07407AC2A33515B24840F5D202F825150740772F3703FBB1484004BC5A81FC140740AD6EF385EFB1484041321AA0A01607407C81FC419FB14840B2E03747831807408382C1F940B148404E896610821A074014A2E7A9E1B04840F2B29DAA9E1C0740FB68B8317AB048405E9A86E1F41D074088AE525338B04840BD501DF8D71F0740E5C4445EDCAF484059EA44A2382007404F176567C8AF484076E6DF287F200740D40D6A08B9AF484043C1D56FE621074050148E0D67AF484086D4E82A33230740B9C1830125AF48405AAC0A096A230740C5A5544D24AF484056DC7E5590230740BCFD3DBE22AF4840654293149E230740E5FFFCAE21AF4840D9068EA6972307405F303DBD1FAF4840F93E5E2C00230740C0D16BC91DAF4840ED706BCDDB1C074045D7C7F51BAF484085CADD440C1107404E59544719AF48405B2AFF81D3090740EE0C95DE17AF48402E80849E42FD0640527A4C8314AF4840669A3BBACDFC06406CA8F03514AF48409F1D54E46FEF0640F361FD4C11AF4840471CF8F013D306407870D6160AAF4840E09A555E0CBB06402EE3C3B604AF4840ABCE60B7E9BA0640E7B6700105AF4840AB3D54A9BAB906409ECDE07A04AF48408881378174B80640EDFE952804AF48403E8AABA110A9064081AF0DC300AF4840C32A8B5F7F9E0640426FA105FFAE48409B6DE363269406400F351693FDAE48408390D7C6538F0640102B2D39FCAE48404AE8DDA94C8B06400EE8B4D4FAAE4840EC52F4D6E981064011A61B0AF8AE4840DC04047570800640991E4AA6F7AE48401A8E0F80AE77064021F4FEE5F5AE4840EA4FA871377206400C47B2420BAF4840B33474DC9A710640E0FC520E17AF4840339230911F6A0640E6F3D754A5AF4840B38B822B2C6606403770690AF0AF48409CB90DB3AF61064048727ADD43B04840F5C972E8C45E0640DEC1845579B0484088E093A1B35806403FF230EBE9B0484005A0616E8D580640EAF6F007E9B04840DF16A4830C5806409F1EC482E4B04840060EB3EE9558064032B11689EBB048402970BC9ADE5806405958842AEFB0484045FEBF7AB659064052B840B4F9B04840249873C61D5B06409FE43CD207B14840416CB899F35E0640770FA44961B14840B2696C6DEF5F064011E51F0DCAB1484072A718577E610640D5A40E731FB24840217DE0D9A261064017093B5F24B24840FB261635C56106403DF21A1E29B2484057B18A45CC610640DE85A9972BB2484032E96D61436206404DD52AD72BB24840414C70E4E863064002BAE4B52DB24840FCF273F750650640F16402B930B24840FBA967C93F660640B8B59F2933B24840E15AA2B2806606409ECAC83A34B24840ADF05233C56606406288709735B248404EC6835A366A06400D08F0BE49B24840B3923D61756C0640B825F19559B2484042485917956C06406BC482805AB24840CFF50C3AB66C064062AF0EBE5BB248400182CB3FCD6C0640C7E6F5115DB2484055EC41DDDA6C0640B68219C05EB24840A0339A6AE86C064093CC237661B24840A57D24C6206E064022391CCB65B24840165998F3B2700640DB1D4F656AB2484043E1D8C0387306404F6622BF64B248407BCE753528750640A902DFE861B248400FF6E79214840640D6EC5AD84FB2484030A6D15445850640F3555B6E4EB248405CB17AA0598D0640375F04CA44B24840C95D8E22BB8F0640997617EE41B24840BE49CE991B9506409A5C82043BB248401EBD2E73D39A0640C3170B6F33B2484045443861AB9B06401474F44D32B2484060F522E7D79C06401E4AABE22EB24840227D7F331CA60640649BC89D67B24840F99319E8F5AB0640716B28EA8BB24840A4EDC171C8B10640D59D1E72B0B248409C2A5A1F9DB206408892270761B248402FE22DAFA9B906404952711E4CB24840",
        ),
    )
    fraud_factories.BeneficiaryFraudCheckFactory(user=user)
    fraud_factories.BeneficiaryFraudReviewFactory(user=user, review=fraud_models.FraudReviewStatus.KO)

    _create_gdpr_user(
        users_factories.UserFactory,
        "Connecté Plus de 3 ans avec Iris",
        THREE_YEARS_AGO - relativedelta(months=6),
        "Utilisateur grand public avec Iris, dernière connexion il y plus de 3 ans",
        irisFrance=iris_for_default_address,
    )

    user = _create_gdpr_user(
        users_factories.UserFactory,
        "Email partagé avec un lieu",
        THREE_YEARS_AGO - relativedelta(months=4),
        "Utilisateur grand public dont l'email est dans un lieu, dernière connexion il y plus de 3 ans",
    )
    fraud_factories.BeneficiaryFraudCheckFactory(user=user)
    fraud_factories.BeneficiaryFraudReviewFactory(user=user, review=fraud_models.FraudReviewStatus.KO)
    offerers_factories.VenueFactory(
        bookingEmail=user.email,
        name="Lieu partageant un email avec un utilisateur oublié",
        managingOfferer__name="Structure d'un utilisateur oublié",
    )

    logger.info("created GDPR users")
