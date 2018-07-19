module View exposing (view)

import Date
import Date.Format
import FormatNumber exposing (format)
import FormatNumber.Locales exposing (Locale, usLocale)
import Html exposing (div, form, h1, input, label, option, p, select, text)
import Html.Attributes exposing (class, selected, style, value)
import Html.Events exposing (onInput)
import LineChart exposing (Config)
import LineChart.Area as Area
import LineChart.Axis as Axis
import LineChart.Axis.Intersection as Intersection
import LineChart.Colors as Colors
import LineChart.Container as Container
import LineChart.Dots as Dots
import LineChart.Events as Events
import LineChart.Grid as Grid
import LineChart.Interpolation as Interpolation
import LineChart.Junk as Junk
import LineChart.Legends as Legends
import LineChart.Line as Line
import Model exposing (ChartPoint, Model, SpeedTestResult)
import Update exposing (Msg(Hint, MonthInput, YearInput))


locale : Locale
locale =
    { usLocale
        | positiveSuffix = " Mbps"
        , negativeSuffix = " Mbps"
    }


downloads : Model -> List ChartPoint
downloads model =
    List.map
        (\r -> ChartPoint r.id r.download r.time)
        model.results


uploads : Model -> List ChartPoint
uploads model =
    List.map
        (\r -> ChartPoint r.id r.upload r.time)
        model.results


toMbps : Float -> Float
toMbps speed =
    speed / (10 ^ 6)


formatTimestamp : ChartPoint -> String
formatTimestamp point =
    point.time
        |> Date.fromTime
        |> Date.Format.format "%b. %e, %Y %H:%M"


formatSpeed : ChartPoint -> String
formatSpeed point =
    point.speed
        |> toMbps
        |> format locale


chartConfig : Model -> Config ChartPoint Msg
chartConfig model =
    { y = Axis.full 400 "Mbps" (.speed >> toMbps)
    , x = Axis.none 600 .time
    , container = Container.responsive "speed-test-results"
    , interpolation = Interpolation.monotone
    , intersection = Intersection.atOrigin
    , legends = Legends.byEnding (Junk.label Colors.black)
    , events = Events.hoverMany Hint
    , junk = Junk.hoverMany model.hinted formatTimestamp formatSpeed
    , grid = Grid.default
    , area = Area.normal 0.3
    , line = Line.default
    , dots = Dots.default
    }


renderChart : Model -> Html.Html Msg
renderChart model =
    LineChart.viewCustom
        (chartConfig model)
        [ LineChart.line Colors.pinkLight Dots.none "Download" (downloads model)
        , LineChart.line Colors.blueLight Dots.none "Upload" (uploads model)
        ]


dateHeading : Model -> String
dateHeading model =
    case ( model.start, model.end ) of
        ( Just start, Just end ) ->
            [ start.month, start.year ]
                |> List.map toString
                |> List.map (String.padLeft 2 '0')
                |> String.join "/"

        _ ->
            ""


renderEmpty : Model -> Html.Html Msg
renderEmpty model =
    p
        [ style [ ( "margin-top", "2rem" ) ] ]
        [ text ("No data for " ++ (dateHeading model)) ]


monthOptions : Model -> List (Html.Html Msg)
monthOptions model =
    let
        options : List ( String, String )
        options =
            [ ( "01", "January" )
            , ( "02", "February" )
            , ( "03", "March" )
            , ( "04", "April" )
            , ( "05", "May" )
            , ( "06", "June" )
            , ( "07", "July" )
            , ( "08", "August" )
            , ( "09", "September" )
            , ( "10", "October" )
            , ( "11", "November" )
            , ( "12", "December" )
            ]

        month : String
        month =
            model.start
                |> Maybe.map .month
                |> Maybe.map toString
                |> Maybe.map (String.padLeft 2 '0')
                |> Maybe.withDefault ""

        isSelected : String -> Html.Attribute Msg
        isSelected value =
            if (Debug.log "value" value) == (Debug.log "month" month) then
                selected True
            else
                selected False
    in
        List.map
            (\( v, t ) -> option [ value v, isSelected v ] [ text t ])
            options


dateForm : Model -> Html.Html Msg
dateForm model =
    form
        [ class "ui form" ]
        [ div
            [ class "fields" ]
            [ div
                [ class "ten wide field" ]
                [ label [] [ text "Month" ]
                , select
                    [ class "ui fluid dropdown", onInput MonthInput ]
                    (monthOptions model)
                ]
            , div
                [ class "six wide field" ]
                [ label [] [ text "Year" ]
                , input [ onInput YearInput, value model.form.year ] []
                ]
            ]
        ]


loading : Html.Html Msg
loading =
    div [ class "ui active centered inline loader" ] []


isLoadingDate : Model -> Bool
isLoadingDate model =
    case ( model.start, model.end ) of
        ( Just start, Just end ) ->
            False

        _ ->
            True


view : Model -> Html.Html Msg
view model =
    let
        date : Html.Html Msg
        date =
            if isLoadingDate model then
                loading
            else
                dateForm model

        chart : Html.Html Msg
        chart =
            if model.loading then
                loading
            else if List.isEmpty model.results then
                renderEmpty model
            else
                renderChart model
    in
        div
            [ class "ui grid container" ]
            [ div
                [ class "column sixteen wide" ]
                [ h1
                    [ class "ui dividing header" ]
                    [ text "My Internet Speed "
                    , div [ class "ui horizontal label" ] [ text (dateHeading model) ]
                    ]
                ]
            , div [ class "column four wide" ] [ date ]
            , div [ class "column twelve wide" ] [ chart ]
            ]
