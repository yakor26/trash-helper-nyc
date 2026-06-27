import { Box, Text, Heading, VStack, IconButton, HStack, Icon } from "@chakra-ui/react";
import { IoIosRefresh} from "react-icons/io";
import { PiProhibit } from "react-icons/pi";
import { FiAlertTriangle } from "react-icons/fi";
import { FaQuestionCircle } from "react-icons/fa";
import { IoMdTime } from "react-icons/io";
import { FaRegTrashAlt, FaRecycle, FaLeaf, FaCouch} from "react-icons/fa";
import { useEffect, useState } from "react";
import '@fontsource-variable/vazirmatn/wght.css';
import api from "../utils/api";

export default function StatusSidebar() {
    const [status, setStatus] = useState("");
    const [updatedTime, setUpdatedTime] = useState("");
    const [todayDate, setTodayDate] = useState("");
    
    const getCollectionStatus = async () => {
        try {
            const res = await api.get("/api/collections/status");
            setStatus(res.data.data[0].status);
            setTodayDate(new Date().toDateString());
            setUpdatedTime(new Date().toLocaleTimeString());
        } catch(error) {
            console.log("Error fetching collection status", error);
        }
    };
    useEffect(() => {
        getCollectionStatus();
    }, []);
    
    const statusColors = [
        {status: "DELAYED", color: "red.600", message: "Delayed", icon: <FiAlertTriangle />},
        {status: "ON SCHEDULE", color: "green.600", message: "On Schedule", icon: <IoMdTime />},
        {status: "NOT IN EFFECT", color: "blue.600", message: "Not in Effect", icon: <PiProhibit />},
        {status: "SUSPENDED", color: "orange.600", message: "Suspended", icon: <FiAlertTriangle />},
        {status: "UNKNOWN", color: "gray.600", message: "Unknown", icon: <FaQuestionCircle />}
    ];
    const currentStatus = statusColors.find(ColStatus => ColStatus.status == status);
    const wasteTypes = [
        {icon: <FaRegTrashAlt/>, label: "Trash"},
        {icon: <FaRecycle/>, label: "Recycling"},
        {icon: <FaLeaf/>, label: "Compost"},
        {icon: <FaCouch/>, label: "Large Items"},
    ];

    return (
    <Box bg={"brand.white.100"}
            borderWidth={"thin"}
            borderColor={"gray.500"}
            borderStyle={"solid"}
            borderRadius={"3xl"}
            boxShadow={"2xl"}
            maxWidth={"2xl"}
            px="14"
            py="8"
            position={"relative"}>

        <IconButton
            isRound={true}
            variant="solid"
            bg={"whiteAlpha.400"}
            color={"white"}
            aria-label='Refresh'
            boxSize={"10"}
            icon={<IoIosRefresh/>}
            position={"absolute"}
            right={"16"}
            onClick={getCollectionStatus}/>
        <VStack
            align={"start"}
            bg={"brand.green.600"}
            color={"brand.white.100"}
            borderTopRadius={"3xl"}
            mx={"-14"}
            mt={"-8"}
            px={"14"}
            pt={"7"}
            pb={"4"}>
            <Heading size={"md"} 
            fontFamily={`'Vazirmatn Variable', sans-serif`}>
                NYC Collection Status
            </Heading>
            <Text fontWeight={"bold"}>{todayDate}</Text>
            <Text>Last updated at: {updatedTime}</Text>
            <HStack bg={currentStatus?.color} borderRadius={"3xl"} px={"12"} py={"2"}>
                {currentStatus?.icon}
            <Text  
            fontWeight={"bold"}>
                {currentStatus?.message}
            </Text>
            </HStack>
        </VStack>
        <VStack align={"stretch"} 
        pt={"2"} 
        spacing={"4"} 
        color={"black"} 
        fontSize={"lg"} 
        fontWeight={"bold"}>
            {wasteTypes.map((wasteType) => 
                <HStack key={wasteType.label}>
                    <IconButton
                        isRound={true}
                        variant="solid"
                        bg={"brand.blue.300"}
                        color={"brand.green.600"}
                        aria-label={wasteType.label}
                        boxSize={"10"}
                        icon={wasteType.icon}
                    />
                    <Text>{wasteType.label}</Text>
                </HStack>
            )}
        </VStack>
    </Box>
 
    )
}