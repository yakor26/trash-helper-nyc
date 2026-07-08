import MainSection from "../components/MainSection";
import LoggedOutReminderSidebar from "./LoggedOutReminderSidebar";
import LoggedInReminderSidebar from "./LoggedInReminderSidebar";
import { useAuth } from "../context/AuthContext";
import StatusSidebar from "../components/StatusSidebar";
import type { ReactNode } from "react";
import { VStack, Flex } from "@chakra-ui/react";

interface LayoutProps {
    children: ReactNode
}

export default function BasicLayout({ children }: LayoutProps) {
    const { user } = useAuth();
    return (
        <>
        <Flex gap={6} mx={"auto"} my={"8"} maxW={"container.2xl"} width={"container.xl"}>
            <VStack w={"sm"} flexShrink={0} spacing={"4"} align={"stretch"}>
                {user ? <LoggedInReminderSidebar/>: <LoggedOutReminderSidebar/> }
                <StatusSidebar/>
            </VStack>
        
        <MainSection>
            {children}
        </MainSection>
        
        </Flex>
        </>
    )
}