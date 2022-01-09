import datetime as dt 
from typing import Any, Text, Dict, List
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import difflib


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_say_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #current_state = tracker.current_state()
        #latest_message = current_state["latest_message"]["text"]
        df = pd.read_csv("./coffee_data.csv")
        print("I am inside say recipe")
        intent = tracker.current_state()["latest_message"]["intent"]["name"]
        print(intent)
        coffee_type = ""
        for entity in tracker.current_state()["latest_message"]["entities"] :
            if entity["entity"] == "coffee_type":
                coffee_type = entity["value"]
                break
        if coffee_type == "" :
           dispatcher.utter_message(text=f"لطفا یک با دیگر به طور کامل بنویسید چه نوع قهوه ای")
           return []
        else :
            most_simillar = difflib.get_close_matches(coffee_type, df.coffee_type.values)
            recipe = df.loc[df.coffee_type== most_simillar[0], intent].values[0]
            dispatcher.utter_message(text = recipe)
            return []

        return []
        
class ActionSayPrice(Action):

    def name(self) -> Text:
        return "action_say_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        df = pd.read_csv("./coffee_data.csv")
        print("I am inside say  price")
        intent = tracker.current_state()["latest_message"]["intent"]["name"]
        coffee_type = ""
        for entity in tracker.current_state()["latest_message"]["entities"] :
            if entity["entity"] == "coffee_type":
                coffee_type = entity["value"]
                break
        if coffee_type == "" :
           dispatcher.utter_message(text=f"لطفا یک با دیگر به طور کامل بنویسید چه نوع قهوه ای")
           return []
        else :
            most_simillar = difflib.get_close_matches(coffee_type, df.coffee_type.values)
            price = df.loc[df.coffee_type== most_simillar[0], intent].values[0]
            dispatcher.utter_message(text = f"the price of {most_simillar[0]} is : {price}")
            return []
        

class ActionSayWhatIs(Action):

    def name(self) -> Text:
        return "action_say_what_is"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        df = pd.read_csv("./coffee_data.csv")
        print("I am inside say what is")
        intent = tracker.current_state()["latest_message"]["intent"]["name"]
        coffee_type = ""
        for entity in tracker.current_state()["latest_message"]["entities"] :
            if entity["entity"] == "coffee_type":
                coffee_type = entity["value"]
                break
        if coffee_type == "" :
           dispatcher.utter_message(text=f"لطفا یک با دیگر به طور کامل بنویسید چه نوع قهوه ای")
           return []
        else :
            most_simillar = difflib.get_close_matches(coffee_type, df.coffee_type.values)
            dispatcher.utter_message(text = df.loc[df.coffee_type== most_simillar[0], intent].values[0])
            return []
            
            
class ActionSayHello(Action):

    def name(self) -> Text:
        return "action_say_hello"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"تو گفتی سلام فقط با یک کلام. چطور میتونم در مورد قهوه بهتون راهنمایی کنم")
            
            
            
class ActionSayGoodbye(Action):

    def name(self) -> Text:
        return "action_say_goodbye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"خداحافظ از کمک به شما خوشحال شدم.")
