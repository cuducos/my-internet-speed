module Main exposing (main)

import Date
import Html
import Model exposing (Model)
import Task
import Update exposing (Msg(..), update)
import View exposing (view)


init : Model
init =
    { start = Nothing
    , end = Nothing
    , results = []
    , hinted = []
    , form = { month = "", year = "" }
    , error = Nothing
    , loading = True
    }


cmd : Cmd Msg
cmd =
    Task.perform LoadDate Date.now


main : Program Never Model Msg
main =
    Html.program
        { init = ( init, cmd )
        , update = update
        , view = view
        , subscriptions = always Sub.none
        }
