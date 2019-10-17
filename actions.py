# -*- coding: utf-8 -*-
from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet

import pandas as pd
import numpy as np
df = pd.read_csv('housing_led_2016_base.csv')

# from rasa.actions.action import action
# from rasa.events import SlotSet

class PopulationForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "population_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["area", "start_year", "start_age"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "area": self.from_entity(entity="area", not_intent="chitchat"),
            "start_year": [
                self.from_entity(
                    entity="start_year", intent=["inform", "request_population"]
                ),
                self.from_entity(entity="number"),
            ],
            "end_year": [
                self.from_entity(
                    entity="end_year", intent=["inform", "request_population"]
                ),
                self.from_entity(entity="number"),
            ],
            "start_age": [
                self.from_entity(
                    entity="start_age", intent=["inform", "request_population"]
                ),
                self.from_entity(entity="number"),
            ],
            "end_age": [
                self.from_entity(
                    entity="end_age", intent=["inform", "request_population"]
                ),
                self.from_entity(entity="number"),
            ],
        }

    # USED FOR DOCS: do not rename without updating in docs
    @staticmethod
    def area_db() -> List[Text]:
        """Database of supported areas"""
        return [
            "greater london",
            "inner london",
            "outer london",
            "southwark",
            "wandsworth",
            "bromley",
            "lambeth",
        ]

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer"""
        try:
            int(string)
            return True
        except ValueError:
            return False

    # USED FOR DOCS: do not rename without updating in docs
    def validate_area(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate area value."""
        if value.lower() in self.area_db():
            # validation succeeded, set the value of the "area" slot to value
            return {"area": value}
        else:
            dispatcher.utter_template("utter_wrong_area", tracker)
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"area": None}

    def validate_start_year(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate start_year value."""

        if self.is_int(value) and int(value) >= 2011 and int(value) <= 2050:
            return {"start_year": value}
        else:
            dispatcher.utter_template("utter_wrong_start_year", tracker)
            # validation failed, set slot to None
            return {"start_year": None}

    def validate_end_year(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate end_year value."""

        if self.is_int(value) and int(value) >= 2011 and int(value) <= 2050:
            return {"end_year": value}
        else:
            dispatcher.utter_template("utter_wrong_end_year", tracker)
            # validation failed, set slot to None
            return {"end_year": None}

    def validate_start_age(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate start_age value."""

        if self.is_int(value) and int(value) >= 0 and int(value) <= 90:
            return {"start_age": value}
        else:
            dispatcher.utter_template("utter_wrong_start_age", tracker)
            # validation failed, set slot to None
            return {"start_age": None}

    def validate_end_age(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate end_age value."""

        if self.is_int(value) and int(value) >= 0 and int(value) <= 90:
            return {"end_age": value}
        else:
            dispatcher.utter_template("utter_wrong_end_age", tracker)
            # validation failed, set slot to None
            return {"end_age": None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        # set up the variables
        area            = tracker.get_slot("area")
        start_year      = tracker.get_slot("start_year")
        end_year        = tracker.get_slot("end_year")
        start_age       = tracker.get_slot("start_age")
        end_age         = tracker.get_slot("end_age")
        single_year     = False
        # if the user has entered a start_age/start_year but no end_age/end_year then assume they are only interested in a single age/year
        # makes the age/year range the same start and end.
        # flag a single due to a quirk with the squeeze() function
        if not end_year:
            end_year = start_year
            single_year = True
        if not end_age:
            end_age = start_age
        # convert variables to strings so that they can be used with Pandas
        start_age = str(start_age)
        end_age = str(end_age)
        # restrict the df to only the desired area
        df_temp = df[df['district'] == area].copy()
        df_temp = df_temp.reset_index(drop=True)
        # we will extract the age range by index and create a sub-set df
        start_age_index = df_temp[df_temp['age']==start_age].index.values.astype(int)
        start_age_index = start_age_index[0]
        end_age_index = df_temp[df_temp['age']==end_age].index.values.astype(int)
        end_age_index = end_age_index[0]
        df_temp = df_temp.loc[start_age_index:end_age_index]
        # do the same for year range
        start_year = str(start_year)
        end_year = str(end_year)
        start_year_index = df_temp[start_year].index.values.astype(int)
        start_year_index = start_year_index[0]
        end_year_index = df_temp[end_year].index.values.astype(int)
        end_year_index = end_year_index[0]+1
        df_temp = df_temp.loc[:, start_year:end_year]
        # make a sum of the age range for each year
        df_temp.loc['total']= df_temp.sum()
        # OK. This is strange but 
        # squeeze converts columns or rows into a series
        # but if the array has a single column then it is converted into a scalar
        # so the two cases need to be handled separately. I couldn't find any other way of solving this
        if single_year:
            df_temp.insert(loc=0, column='year', value=start_year)
            df_temp = df_temp.tail(1)
            df_temp = df_temp.T.squeeze()
            df_temp = df_temp.tail(1)
        else:
            df_temp = df_temp.tail(1)
            df_temp = df_temp.T.squeeze()
        # loop through the data and construct a response
        # I couldn't find a way of looping and sending a separate message using format and variables for each iteration of the loop
        # utter_message would only send the first response in the loop and then stop sending
        loop_response='(Area = ' + area + ' and Age Group = ' + start_age + ' to ' + end_age + '): '
        for year,total in df_temp.items():
            loop_response = loop_response + str(year) + ' total: ' +  str(total) + ' // '
        dispatcher.utter_message(loop_response)
        return[]