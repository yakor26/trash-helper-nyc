import { Box, Text, Heading, Button, ButtonGroup, HStack, Icon, VStack } from "@chakra-ui/react"
import { FaBell } from "react-icons/fa"
export default function ScheduleSidebar() {
    return (
    <>
    <Box bg={"brand.white.100"} 
            borderWidth={"thin"} 
            borderColor={"gray.500"} 
            borderStyle={"solid"} 
            borderRadius={"lg"} 
            boxShadow={"2xl"}
            maxWidth={"2xl"}
            p={"10"}>
    <HStack>
    <Icon as={FaBell} boxSize={"auto"} color={"yellow.800"}/>
    </HStack>
    <VStack>
    <Heading size={"md"}>Get Sanitation Collection Reminders</Heading>
    <Text>Sign up to receive text reminders before your pickup day.</Text>
    <ButtonGroup variant={"solid"}>
        <Button bg="brand.orange.400">Create Account</Button>
        <Button bg="gray.200">Login</Button>
    </ButtonGroup>
    </VStack>
    </Box>
    </>
    )
}