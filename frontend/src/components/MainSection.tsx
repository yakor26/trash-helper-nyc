import { Box, Text } from "@chakra-ui/react"
import type { ReactNode } from "react"

interface MainSectionProps {
    children: ReactNode
}
export default function MainSection({ children }: MainSectionProps ) {
    return (
    <>
    <Box bg={"brand.white.100"} 
            borderWidth={"thin"} 
            borderColor={"gray.500"} 
            borderStyle={"solid"} 
            borderRadius={"lg"} 
            boxShadow={"2xl"}
            width={"3xl"}
            p={10}
            >

    <Text>Main Section placeholder</Text>
    {children}
    </Box>
    </>
    )
}