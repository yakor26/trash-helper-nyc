import { Box, Text, Heading, Button, Icon, VStack } from "@chakra-ui/react";
import { FaBell } from "react-icons/fa";
import { Link as ReactRouterLink } from "react-router";
import { useAuth } from "../context/AuthContext";

export default function LoggedInReminderSidebar() {
    const { user } = useAuth();
    const allowsNotifications = user?.allow_notifications
    return (
    <Box bg={"brand.white.100"} 
            borderWidth={"thin"} 
            borderColor={"gray.500"} 
            borderStyle={"solid"} 
            borderRadius={"3xl"} 
            boxShadow={"2xl"}
            maxWidth={"2xl"}
            px={"14"}
            py={"8"}
            position={"relative"}
            >
        <Icon as={FaBell} 
        boxSize={"6"} 
        color={"yellow.800"} 
        position={"absolute"}
        top={"8"}
        left={"6"}
        />
    <VStack spacing={"3"} align={"left"}>
        <Heading size={"md"}>Text reminders are {allowsNotifications ? <>enabled</>: <>disabled</>} </Heading>
        <Text fontWeight={"normal"}>Text alerts are sent at 8PM the night before sanitation pickup.</Text>
            <Button bg="brand.blue.300" 
            borderRadius={"3xl"} 
            px={"16"} 
            as={ReactRouterLink}
            to={"/profile"}
            _hover={{ bg: "blackAlpha.400" }}>
                Manage Settings</Button>
    </VStack>
    
    </Box>
    )
}