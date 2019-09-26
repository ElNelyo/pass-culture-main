import pandas

from models.db import db


def get_all_beneficiary_users_details():
    connection = db.engine.connect()

    beneficiary_users_details = pandas.concat(
        [
            get_experimentation_session_column(connection),
            get_department_column(connection),
            get_activation_date_column(connection),
            get_typeform_filling_date(connection),
            get_first_connection(connection)
        ],
        axis=1
    )
    beneficiary_users_details = beneficiary_users_details.reset_index(drop=True)
    return beneficiary_users_details


def get_experimentation_session_column(connection):
    query = '''
    SELECT 
     CASE 
      WHEN booking."isUsed" THEN 1
      ELSE 2 
     END AS "Vague d'expérimentation",
     "user".id AS user_id
    FROM "user"
    LEFT JOIN booking ON booking."userId" = "user".id
    LEFT JOIN stock ON stock.id = booking."stockId"
    LEFT JOIN offer 
     ON offer.id = stock."offerId" 
     AND offer.type = 'ThingType.ACTIVATION'
    WHERE "user"."canBookFreeOffers"
    '''
    return pandas.read_sql_query(query, connection, index_col="user_id")


def get_department_column(connection):
    query = '''
    SELECT 
     "user"."departementCode" AS "Département",
     "user".id AS user_id
    FROM "user"    
    WHERE "user"."canBookFreeOffers"
    '''
    return pandas.read_sql(query, connection, index_col="user_id")


def get_activation_date_column(connection):
    query = '''
    WITH validated_activation_booking AS (
     SELECT activity.issued_at, booking."userId" 
     FROM activity 
     JOIN booking   
      ON (activity.old_data ->> 'id')::int = booking.id 
      AND booking."isUsed" 
     JOIN stock 
      ON stock.id = booking."stockId" 
     JOIN offer 
      ON stock."offerId" = offer.id 
      AND offer.type = 'ThingType.ACTIVATION' 
     WHERE  
      activity.table_name='booking'   
      AND activity.verb='update'   
      AND activity.changed_data ->> 'isUsed'='true' 
    )

    SELECT 
     CASE 
      WHEN booking."isUsed" THEN validated_activation_booking.issued_at
      ELSE "user"."dateCreated"
     END AS "Date d'activation",
     "user".id as user_id
    FROM "user"
    LEFT JOIN booking ON booking."userId" = "user".id
    LEFT JOIN stock ON stock.id = booking."stockId"
    LEFT JOIN offer ON offer.id = stock."offerId" 
    LEFT JOIN validated_activation_booking 
     ON validated_activation_booking."userId" = "user".id
     AND offer.type = 'ThingType.ACTIVATION'
    WHERE "user"."canBookFreeOffers"
    '''
    return pandas.read_sql(query, connection, index_col='user_id')


def get_typeform_filling_date(connection):
    query = '''
    WITH typeform_filled AS (
     SELECT activity.issued_at, "user".id AS user_id, "user"."canBookFreeOffers"
     FROM "user" 
     LEFT JOIN "activity"    
      ON (activity.old_data ->> 'id')::int = "user".id  
      AND activity.table_name='user'    
      AND activity.verb='update'    
      AND activity.changed_data ->> 'needsToFillCulturalSurvey'='false'
      )
      
    SELECT 
     typeform_filled.issued_at AS "Date de remplissage du typeform",
     typeform_filled.user_id AS user_id
    FROM typeform_filled
    WHERE typeform_filled."canBookFreeOffers"
    '''
    return pandas.read_sql(query, connection, index_col='user_id')


def get_first_connection(connection):
    query = '''
    WITH recommendation_dates AS (
     SELECT 
      MIN(recommendation."dateCreated") AS first_recommendation_date, 
      "user".id AS user_id,
      "user"."canBookFreeOffers"
     FROM "user"
     LEFT JOIN recommendation ON recommendation."userId" = "user".id 
     GROUP BY "user".id 
    )
    
    SELECT 
     recommendation_dates.first_recommendation_date AS "Date de première connection",
     recommendation_dates.user_id AS user_id
    FROM recommendation_dates
    WHERE recommendation_dates."canBookFreeOffers"
    '''

    return pandas.read_sql(query, connection, index_col='user_id')
