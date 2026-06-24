import { Outlet } from "react-router"
import { useState } from "react"
import BasicLayout from "../components/BasicLayout"
import ExampleItems from "../components/ExampleItems"
import SearchResult from "../components/SearchResult"
import type { Category } from "../utils/helper"
import api from "../utils/api"
import { 
    Box, 
    Heading, 
    Stack, 
    Input, 
    InputGroup, 
    InputLeftAddon, 
    Icon, 
    Button, 
    Grid, 
    GridItem,
    HStack
} from "@chakra-ui/react"
import { FaSearch } from "react-icons/fa";

export default function SearchPage() {
    const [searchQuery, setSearchQuery] = useState<string>("")
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [result, setResult] = useState<Category[]>([])
    const handleSearchQuery = async (value: string) => {
        try {
            setSearchQuery(value)
            const res = await api.get(`/api/item-categories?search=${value}`)
            console.log(res.data.data)
            const data_result = res.data.data
            setResult(data_result)
        } catch(error) {
            console.log("Failed to search", error)
    }
    }
    return (
        <>
        <BasicLayout>
        <Stack spacing={4}>
            <Heading size={"lg"}>What item you throwing away?</Heading>
            <Heading size={"sm"} color={"teal.700"}>Search for an item to get instructions on proper disposal.</Heading>
            <InputGroup size={"lg"} boxShadow={"md"} borderRadius={"xl"} borderColor={"blackAlpha.500"}>
                <InputLeftAddon bg={"brand.white.100"} borderRightColor={"transparent"}><Icon as={FaSearch} color={"teal.600"}/></InputLeftAddon>
                <Input type='text' 
                value={searchQuery} 
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder='ex. pizza box' 
                size={"lg"}/>
            </InputGroup>
            <Heading size={"md"} color={"blackAlpha.700"} py={"5"}>Example Search Items</Heading>
    
        <Grid 
        templateRows='repeat(2, 1fr)'
        templateColumns='repeat(2, 1fr)'
        gap={3}>
        
        {!searchQuery ? 
        <ExampleItems 
            onSearchClick={setSearchQuery} 
            onSearchSubmit={handleSearchQuery}/>: 
        <SearchResult 
            data={result}/>
        }

        </Grid>
        </Stack>
        <Outlet/>
        </BasicLayout>
        </>

    )
}