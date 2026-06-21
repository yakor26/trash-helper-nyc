import MainSection from "../components/MainSection"
import ScheduleSidebar from "../components/ScheduleSidebar"
import StatusSidebar from "../components/StatusSidebar"
import type { ReactNode } from "react"
import { HStack, VStack, Box, Flex } from "@chakra-ui/react"

interface LayoutProps {
    children: ReactNode
}
export default function BasicLayout({ children }: LayoutProps) {
    return (
        <>
        <Flex gap={"6"} mx={"auto"} my={"8"} maxW={"container.xl"}>
            <Box w={"lg"}>
                <ScheduleSidebar/>
                <StatusSidebar/>
            </Box>
        
        <MainSection>
            {children}
        </MainSection>
        
        </Flex>
        </>

    )
}