CREATE VIEW mart.vw_citizens_anon AS
SELECT
    fake_citizen_id
    , age
    , family_index_number
    , is_living_alone
    , is_elder_pair
    , has_phone
    , has_mobile_phone
    , is_welfare_patient
    , is_new_imigrant
    , has_breath_troubles
    , is_hazramim
    , is_in_hamal_batch
    , file_name_hamal
    , is_dead_hamal
    , is_left_the_city_permanent
    , is_answered_the_call
    , is_final_status
    , is_lonely 
    , is_address_wrong
    , has_mamad
    , has_miklat_prati
    , has_miklat_ziburi
    , has_mobility_restriction
    , has_temporary_address
    , is_temporary_abroad
    , appearance_count
    , calcenter_case_number
FROM mart.citizens;