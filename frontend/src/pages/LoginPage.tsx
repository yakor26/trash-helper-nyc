import { 
    Heading, 
    Box, 
    FormControl, 
    FormLabel, 
    Icon, 
    Input, 
    Button, 
    InputGroup, 
    InputRightElement, 
    IconButton, 
    VStack, 
    HStack, 
    Alert, 
    AlertIcon
} from "@chakra-ui/react";
import { MdOutlinePerson } from "react-icons/md";
import { FaLock } from "react-icons/fa";
import { Link as ReactLink, useNavigate } from "react-router";
import { useState } from "react";
import { FiEye, FiEyeOff } from "react-icons/fi";
import api from "../utils/api";

export default function LoginPage() {
    const [showPassword, setShowPassword] = useState<boolean>(false);
    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [loginError, setLoginError] = useState<string>("");
    const navigate = useNavigate();
    const togglePassword = () => setShowPassword(!showPassword);

    const handleLogin = async () => {
        try {
            setIsLoading(true);
            setLoginError("");
            // const data = await api.post("/login", { username, password});
            navigate("/search");

        } catch(error) {
            setLoginError("Invalid Username or Password");
        } finally {
            setIsLoading(false);
        }
    };
    return (
        <>
        <VStack minH={"100vh"} alignItems={"center"} justifyContent={"center"}>
            <VStack spacing={4} pb={4}>
            <Heading size={"lg"}>Welcome Back</Heading>
            <Heading 
                size={"md"} 
                fontWeight={"medium"} 
                color={"gray.600"}>
                    Sign into your account
                </Heading>
            </VStack>
        {loginError && <Alert status="error" width={"md"}><AlertIcon/>{loginError}</Alert>}
        <Box 
            bg={"brand.white.100"} 
            p={12} 
            borderRadius={"3xl"} 
            w={"lg"} 
            boxShadow={"md"} 
            minH={"md"}>
            <VStack spacing={6}>
            <FormControl>
                <HStack mb={2}>
                <Icon as={MdOutlinePerson} boxSize={6} color={"gray.600"}/>
                <FormLabel mb={0}>Username</FormLabel>
                </HStack>
                <Input type='text'
                placeholder="Enter username"
                value={username}
                size={"lg"}
                onChange={(e) => setUsername(e.target.value)}
                variant={"filled"}/>
                
            </FormControl>

            <FormControl>
                <HStack mb={2}>
                <Icon as={FaLock} boxSize={6} color={"gray.600"}/>
                <FormLabel mb={0}>Password</FormLabel>
                </HStack>
                <InputGroup>
                    <Input
                    placeholder="Enter password"
                    value={password}
                    size={"lg"}
                    type={showPassword ? 'text' : 'password'}
                    onChange={(e) => setPassword(e.target.value)}
                    variant={"filled"}/>
                    <InputRightElement>
                    {showPassword ? 
                    <IconButton 
                        aria-label="Show Password" 
                        size={"sm"}
                        _hover={"none"}
                        icon={<FiEyeOff/>} 
                        onClick={togglePassword}/>:
                    <IconButton 
                        aria-label="Show Password" 
                        size={"sm"}
                        _hover={"none"}
                        icon={<FiEye/>} 
                        onClick={togglePassword}/>
                    }
                    </InputRightElement>
                </InputGroup>
            </FormControl>
            
                <Button 
                as={ReactLink}
                isLoading={isLoading}
                bg={"brand.orange.400"}
                color={"brand.white.100"}
                fontWeight={"extrabold"}
                spinnerPlacement="start"
                w={"full"}
                p={6}
                onClick={handleLogin}>
                    Log In
                </Button>
            </VStack>
        </Box>
        </VStack>

        
        </>

    )
}