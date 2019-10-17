## request_housing without greeting
* request_housing
    - utter_request_housing
    - action_restart

## request_housing with greeting
* greet
    - utter_greet
* request_housing
    - utter_request_housing
    - action_restart

## request_population with greeting
* greet
    - utter_greet
* request_population
    - population_form
    - form{"name": "population_form"}
    - form{"name": null}
    - utter_slots_values
    - action_restart

## request_population without greeting
* request_population
    - population_form
    - form{"name": "population_form"}
    - form{"name": null}
    - utter_slots_values
    - action_restart

## happy path with Stop Graham
* request_population
    - population_form
    - form{"name": "population_form"}
* stop
    - action_deactivate_form
    - action_restart

## unhappy path
* greet
    - utter_greet
* request_population
    - population_form
    - form{"name": "population_form"}
* chitchat
    - utter_chitchat
    - population_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## very unhappy path
* greet
    - utter_greet
* request_population
    - population_form
    - form{"name": "population_form"}
* chitchat
    - utter_chitchat
    - population_form
* chitchat
    - utter_chitchat
    - population_form
* chitchat
    - utter_chitchat
    - population_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## stop but continue path
* greet
    - utter_greet
* request_population
    - population_form
    - form{"name": "population_form"}
* stop
    - utter_ask_continue
* affirm
    - population_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## stop and really stop path
* greet
    - utter_greet
* request_population
    - population_form
    - form{"name": "population_form"}
* stop
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}

## chitchat stop but continue path
* request_population
    - population_form
    - form{"name": "population_form"}
* chitchat
    - utter_chitchat
    - population_form
* stop
    - utter_ask_continue
* affirm
    - population_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## stop but continue and chitchat path
* greet
    - utter_greet
* request_population
    - population_form
    - form{"name": "population_form"}
* stop
    - utter_ask_continue
* affirm
    - population_form
* chitchat
    - utter_chitchat
    - population_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## chitchat stop but continue and chitchat path
* greet
    - utter_greet
* request_population
    - population_form
    - form{"name": "population_form"}
* chitchat
    - utter_chitchat
    - population_form
* stop
    - utter_ask_continue
* affirm
    - population_form
* chitchat
    - utter_chitchat
    - population_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## chitchat, stop and really stop path
* greet
    - utter_greet
* request_population
    - population_form
    - form{"name": "population_form"}
* chitchat
    - utter_chitchat
    - population_form
* stop
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}

## bot challenge
* bot_challenge
  - utter_iamabot
