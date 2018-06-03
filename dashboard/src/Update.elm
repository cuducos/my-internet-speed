module Update exposing (Msg(..), update)

import Date exposing (Date, Month(..))
import Date.Format
import Decoder exposing (decodeResults)
import Http
import Model exposing (ChartPoint, Form, Model, SpeedTestResult, SpeedTestResults)


type Msg
    = LoadResults (Result Http.Error SpeedTestResults)
    | MonthInput String
    | YearInput String
    | LoadDate Date
    | Hint (List ChartPoint)


startMonth : Date -> Maybe Model.Month
startMonth date =
    let
        month : Int
        month =
            case Date.month date of
                Jan ->
                    1

                Feb ->
                    2

                Mar ->
                    3

                Apr ->
                    4

                May ->
                    5

                Jun ->
                    6

                Jul ->
                    7

                Aug ->
                    8

                Sep ->
                    9

                Oct ->
                    10

                Nov ->
                    11

                Dec ->
                    12
    in
        date
            |> Date.year
            |> Model.Month month
            |> Just


addMonth : Model.Month -> Model.Month
addMonth date =
    if date.month <= 11 then
        Model.Month (date.month + 1) date.year
    else
        Model.Month 1 (date.year + 1)


endMonth : Date -> Maybe Model.Month
endMonth date =
    date
        |> startMonth
        |> Maybe.map addMonth


defaultUrl : String
defaultUrl =
    "http://0.0.0.0:3001/result"


filteredUrl : Model.Month -> Model.Month -> String
filteredUrl start end =
    String.concat
        [ defaultUrl
        , "?and=("
        , "timestamp.gte."
        , start.year |> toString
        , "-"
        , start.month |> toString |> String.padLeft 2 '0'
        , "-"
        , "01"
        , ","
        , "timestamp.lt."
        , end.year |> toString
        , "-"
        , end.month |> toString |> String.padLeft 2 '0'
        , "-"
        , "01)"
        ]


url : Model -> String
url model =
    case ( model.start, model.end ) of
        ( Just start, Just end ) ->
            filteredUrl start end

        _ ->
            defaultUrl


loadResults : Model -> Cmd Msg
loadResults model =
    Http.send
        LoadResults
        (Http.get (url model) decodeResults)


updateFromForm : Model -> ( Model, Cmd Msg )
updateFromForm model =
    let
        newYear : Result String Int
        newYear =
            String.toInt model.form.year

        newMonth : Result String Int
        newMonth =
            String.toInt model.form.month
    in
        case ( newYear, newMonth ) of
            ( Ok year, Ok month ) ->
                [ year, month, 2 ]
                    |> List.map toString
                    |> Debug.log "1"
                    |> List.map (String.padLeft 2 '0')
                    |> Debug.log "2"
                    |> String.join "-"
                    |> Debug.log "3"
                    |> Date.fromString
                    |> Debug.log "4"
                    |> Result.map (\d -> update (LoadDate d) model)
                    |> Debug.log "5"
                    |> Result.withDefault (model ! [])

            _ ->
                let
                    _ =
                        Debug.log "error" model
                in
                    model ! []


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        LoadDate date ->
            let
                form : Model.Form
                form =
                    { month = Date.Format.format "%m" date
                    , year = Date.Format.format "%Y" date
                    }

                newModel : Model
                newModel =
                    { model
                        | loading = True
                        , start = startMonth date
                        , end = endMonth date
                        , form = form
                    }
            in
                newModel ! [ loadResults newModel ]

        YearInput value ->
            let
                form : Model.Form
                form =
                    model.form

                newModel : Model
                newModel =
                    { model | form = { form | year = value } }
            in
                updateFromForm newModel

        MonthInput value ->
            let
                form : Model.Form
                form =
                    model.form

                newModel : Model
                newModel =
                    { model | form = { form | month = value } }
            in
                updateFromForm newModel

        LoadResults (Ok results) ->
            { model | results = results, loading = False, error = Nothing } ! []

        LoadResults (Err error) ->
            { model | error = Just error, loading = False } ! []

        Hint results ->
            { model | hinted = results } ! []
