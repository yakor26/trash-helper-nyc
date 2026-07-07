import { Box, Text, Heading, Button, ButtonGroup, Icon, VStack } from "@chakra-ui/react";
import { FaBell } from "react-icons/fa";
import { Link as ReactRouterLink } from "react-router";

export default function BasicSidebar() {
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
        <Heading size={"md"}>Get Sanitation Collection Reminders</Heading>
        <Text>Sign up to receive text reminders before your pickup day.</Text>
        <ButtonGroup variant={"solid"} spacing={"2"}>
            <Button bg="brand.orange.400" 
            borderRadius={"3xl"} 
            px={"8"}
            as={ReactRouterLink}
            to={"/register"}
            _hover={{ bg: "blackAlpha.300" }}>
                Create Account</Button>
            <Button bg="brand.blue.300" 
            borderRadius={"3xl"} 
            px={"16"} 
            as={ReactRouterLink}
            to={"/login"}
            _hover={{ bg: "blackAlpha.400" }}>
                Login</Button>
        </ButtonGroup>
    </VStack>
    
    </Box>
    )
}