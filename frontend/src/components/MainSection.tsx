import { Box } from "@chakra-ui/react";
import type { ReactNode } from "react";

interface MainSectionProps {
    children: ReactNode;
}
export default function MainSection({ children }: MainSectionProps ) {
    return (
    <Box bg={"brand.white.100"} 
            borderWidth={"thin"} 
            borderColor={"gray.500"} 
            borderStyle={"solid"} 
            borderRadius={"3xl"} 
            boxShadow={"2xl"}
            width={"container.xl"}
            p={20}
            >

    {children}
    </Box>
    )
}