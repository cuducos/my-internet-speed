module Model exposing (ChartPoint, Form, Model, Month, SpeedTestResult, SpeedTestResults)

import Http
import Time exposing (Time)


type alias SpeedTestResult =
    { id : Int
    , time : Time
    , download : Float
    , upload : Float
    , ping : Float
    }


type alias SpeedTestResults =
    List SpeedTestResult


type alias ChartPoint =
    { id : Int
    , speed : Float
    , time : Time
    }


type alias Month =
    { month : Int
    , year : Int
    }


type alias Form =
    { month : String
    , year : String
    }


type alias Model =
    { start : Maybe Month
    , end : Maybe Month
    , results : SpeedTestResults
    , hinted : List ChartPoint
    , form : Form
    , error : Maybe Http.Error
    , loading : Bool
    }
