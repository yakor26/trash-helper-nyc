import { Box, Text, Heading } from "@chakra-ui/react"
export default function StatusSidebar() {
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
        <Heading size={"md"}>NYC Collection Status</Heading>
        <Text>Sunday, June 21, 2026</Text>
        <Text>Trash</Text>
        <Text>Recycling</Text>
        <Text>Compost</Text>
        <Text>Large Items</Text>
    </Box>
    </>
    )
}