import { Outlet } from "react-router"
import BasicLayout from "../components/BasicLayout"
import { Box, Heading, Stack, Input, InputGroup, InputLeftAddon, Icon } from "@chakra-ui/react"
import { FaSearch } from "react-icons/fa"

export default function SearchPage() {
    return (
        <>
        <BasicLayout>
        <Stack spacing={4}>
            <Heading size={"md"}>What item you throwing away?</Heading>
            <Heading size={"sm"} color={"blackAlpha.700"}>Search for an item to get instructions on proper disposal.</Heading>
            <InputGroup size={"lg"} boxShadow={"md"} borderRadius={"xl"} borderColor={"blackAlpha.500"}>
                <InputLeftAddon bg={"brand.white.100"} borderRightColor={"transparent"}><Icon as={FaSearch}/></InputLeftAddon>
                <Input type='text' placeholder='ex. pizza box' size={"lg"}/>
             
            </InputGroup>
            <Heading size={"sm"} color={"blackAlpha.700"}>Commonly Search Items</Heading>
        <Outlet/>
        </Stack>
        </BasicLayout>
        
        </>

    )
}