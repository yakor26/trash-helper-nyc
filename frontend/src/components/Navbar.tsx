import { Box, HStack, Flex, Heading, Icon } from "@chakra-ui/react"
import { Link as ChakraLink } from "@chakra-ui/react"
import { Link as ReactRouterLink } from "react-router"
import { FaRecycle } from "react-icons/fa"

export default function Navbar() {
    return (
        <Box bg="brand.green.600" color="brand.white.100" px={3} py={3} position="sticky" top={0} zIndex="sticky">
            <Flex justify="space-around">

                <HStack spacing="1">
                    <Box border="1" borderColor="gray.200" bg="whiteAlpha.400" boxShadow="xl" px={3} py={2} borderRadius="full">
                        <Icon as={FaRecycle} boxSize={9} color="brand.white.100" />
                    </Box>
                    <ChakraLink as={ReactRouterLink} to="/" _hover={{ textDecoration: "none" }}>
                        <Heading size="lg">Trash Guide NYC</Heading>
                    </ChakraLink>
                </HStack>

                <HStack spacing={10}>
                    <ChakraLink as={ReactRouterLink} to="/schedule" fontSize="2xl" px={7} py={1} _hover={{ bg: "whiteAlpha.400", textDecoration: "none" }}>
                        Schedule
                    </ChakraLink>
                    <ChakraLink as={ReactRouterLink} to="/search" fontSize="2xl" px={7} py={1} _hover={{ bg: "whiteAlpha.400", textDecoration: "none" }}>
                        Search
                    </ChakraLink>
                    <ChakraLink as={ReactRouterLink} to="/login" fontSize="2xl" border={1} bg="brand.orange.400" borderRadius="full" px={7} py={1} _hover={{ bg: "orange.300", textDecoration: "none" }}>
                        Login
                    </ChakraLink>
                </HStack>

            </Flex>
        </Box>
    )
}