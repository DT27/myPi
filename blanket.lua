--
-- 自动控制电热毯开关
--
commandArray = {}

print ("All based event fired");
-- loop through all the devices
for deviceName,deviceValue in pairs(otherdevices) do
    if (deviceName=='电热毯(s3)') then
        if (timeofday['Nighttime']) and otherdevices["OnePlus3"] == "On" then
            if deviceValue == "On" and uservariables['bedroomTemp'] >= 20 then
                -- print("电热毯处于打开状态")
                -- print("当前室内温度："..tostring(uservariables['bedroomTemp']))
                -- print("温度适宜，关闭电热毯")
                commandArray['电热毯(s3)'] = "Off"
                commandArray['Variable:blanket']='off'
            elseif deviceValue == "Off" and uservariables['bedroomTemp'] < 20 then
                -- print("电热毯处于关闭状态")
                -- print("当前室内温度："..tostring(uservariables['bedroomTemp']))
                -- print("温度偏低，打开电热毯")
                commandArray['电热毯(s3)'] = "On"
                commandArray['Variable:blanket']='on'
            end
        else
            if deviceValue == "On" then
                commandArray['电热毯(s3)'] = "Off"
                commandArray['Variable:blanket']='off'
            end
        end
    end
end

return commandArray
