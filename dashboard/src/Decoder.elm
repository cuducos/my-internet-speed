module Decoder exposing (decodeResults)

import Date exposing (Date)
import Json.Decode exposing (Decoder, field, float, int, string)
import Model exposing (SpeedTestResult, SpeedTestResults)
import Time exposing (Time)


timestamp : Decoder Time
timestamp =
    Json.Decode.andThen toTime string


toTime : String -> Decoder Time
toTime value =
    case Date.fromString value of
        Ok date ->
            Json.Decode.succeed (Date.toTime date)

        Err _ ->
            [ "Cannot decode ", value, " as a timestamp" ]
                |> String.concat
                |> Json.Decode.fail


decodeResult : Decoder SpeedTestResult
decodeResult =
    Json.Decode.map5 SpeedTestResult
        (field "id" int)
        (field "timestamp" timestamp)
        (field "download" float)
        (field "upload" float)
        (field "ping" float)


decodeResults : Decoder SpeedTestResults
decodeResults =
    Json.Decode.list decodeResult
