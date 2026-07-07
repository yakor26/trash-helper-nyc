import { useSearchParams } from "react-router";
import { useEffect, useState } from "react";
import BasicLayout from "../components/BasicLayout";
import ExampleItems from "../components/ExampleItems";
import SearchResult from "../components/SearchResult";
import type { ItemCategory } from "../utils/helper";
import {api} from "../utils/api";
import { useAuth } from "../context/AuthContext";
import {
    Box,
    Heading,
    Stack,
    Input,
    InputGroup,
    InputRightElement,
    Grid,
    HStack,
    IconButton,
    Spinner,
    Center
} from "@chakra-ui/react";
import { FaSearch } from "react-icons/fa";
import { IoClose } from "react-icons/io5";

export default function SearchPage() {
    const [searchQuery, setSearchQuery] = useState<string>("");
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [result, setResult] = useState<ItemCategory[]>([]);
    const [isSearchDone, setIsSearchDone] = useState<boolean>(false);
    const [searchParams, setSearchParams] = useSearchParams();
    const { user } = useAuth();

    useEffect(() => {
        // for /search with no parameters reset
        if (!searchParams.get("query")) {
            setSearchQuery("")
            setIsSearchDone(false)
        }
    }, [searchParams]);
    
    const handleSearchQuery = async (value: string = searchQuery) => {
        try {
            setSearchQuery(value);
            setIsLoading(true);
            const res = await api.get(`/api/item-categories?search=${value}`);
            const data_result = res.data.data;
            setSearchParams(`?query=${value}`);
            setResult(data_result);
            setIsSearchDone(true);
        } catch(error) {
            console.log("Failed to search", error);
        } finally {
            setIsLoading(false);
        }
    };
    return (
        <>
        <BasicLayout>
        <Stack spacing={4}>
            {user?.username ? <Heading size={"md"} color={"gray.600"}>Welcome Back, {user.username}</Heading>: null}
            <Heading size={"lg"}>What item you throwing away?</Heading>
            <Heading size={"sm"} color={"teal.700"}>Search for an item to get instructions on proper disposal.</Heading>
            <HStack>
            <InputGroup size={"lg"} boxShadow={"md"} borderRadius={"xl"} borderColor={"blackAlpha.500"}>
                <Input type='text' 
                value={searchQuery} 
                onChange={
                    (e) => 
                    {setSearchQuery(e.target.value)
                    setIsSearchDone(false)
                }}
                onKeyDown={
                    (e) => { if(e.key === "Enter") {
                        handleSearchQuery()
                    }
                }}
                placeholder='ex. pizza box' 
                size={"lg"}
                borderRightRadius={"none"}/>
                <InputRightElement>
                 <IconButton 
                 aria-label="clear" 
                 bg={"transparent"}
                 _hover={"none"}
                 onClick={() => {
                    setSearchQuery("")
                    setSearchParams("")
                }}
                 icon={<IoClose/>}/>
                </InputRightElement>
                
            </InputGroup>
            <IconButton 
                    aria-label="Search" 
                    color={"teal.600"} 
                    icon={<FaSearch/>}
                    variant={"outline"}
                    borderColor={"blackAlpha.500"} 
                    bg={"gray.200"}
                    borderLeftRadius={"none"}
                    size={"lg"}
                    p={6}
                    ml={-3}
                    onClick={() => handleSearchQuery()}
                    />
            </HStack>

        {searchQuery && isLoading && <Center><Spinner size={"lg"} /></Center>}

        {searchQuery && !isLoading && isSearchDone &&
            <SearchResult data={result}/>
        }

        {!searchQuery &&
        <Box>
        <Heading size={"md"} color={"blackAlpha.700"} py={"5"}>Example Search Items</Heading>
        <Grid
        templateRows='repeat(2, 1fr)'
        templateColumns='repeat(2, 1fr)'
        gap={3}>
            <ExampleItems
                onSearchClick={setSearchQuery}
                onSearchSubmit={handleSearchQuery}/>
            
        </Grid>
        </Box>
        }
        </Stack>
        </BasicLayout>
        </>

    )
}