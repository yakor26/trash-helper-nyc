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
    AlertIcon,
    Text,
    Checkbox,
    CheckboxGroup,
    Link as ChakraLink
} from "@chakra-ui/react";
import { MdOutlinePerson, MdOutlineMail } from "react-icons/md";
import { FaPhone } from "react-icons/fa6";
import { FaLock } from "react-icons/fa";
import { Link as ReactLink, useNavigate } from "react-router";
import { useState } from "react";
import { FiEye, FiEyeOff } from "react-icons/fi";
import { useAuth } from "../context/AuthContext"

export default function RegisterPage() {
    const [username, setUsername] = useState<string>("");
    const [email, setEmail] = useState<string>("");
    const [phoneNumber, setPhoneNumber] = useState<string>("");
    const [allowNotifications, setAllowNotifications] = useState<boolean>(false);
    const [password, setPassword] = useState<string>("");
    const [confirmPassword, setConfirmPassword] = useState<string>("");
    const [showPassword, setShowPassword] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [registerError, setRegisterError] = useState<string>("");
    const { register } = useAuth();
    const navigate = useNavigate();
    const togglePassword = () => setShowPassword(!showPassword);

    const handleRegister = async () => {
        try {
            setIsLoading(true);
            setRegisterError("");
            await register({
                username: username, 
                email: email,
                password: password,
                confirm_password: confirmPassword,
                phone_number: phoneNumber, 
                allow_notifications: allowNotifications,
            })
            navigate("/profile");
        } catch(error) {
            setRegisterError("");
        } finally {
            setIsLoading(false);
        }
    };
    return (
        <>
        <VStack minH={"100vh"} alignItems={"center"} justifyContent={"center"}>
            <VStack spacing={3} pb={4}>
            <Heading size={"lg"} pt={4}>Create Account</Heading>
            <Heading 
                size={"md"} 
                fontWeight={"medium"} 
                color={"gray.600"}>
                    Register a new account
                </Heading>
            </VStack>
        {registerError && <Alert status="error" width={"md"}><AlertIcon/>{registerError}</Alert>}
        <Box 
            bg={"brand.white.100"} 
            p={12} 
            borderRadius={"3xl"} 
            w={"xl"} 
            boxShadow={"md"} 
            minH={"md"}>
            <VStack spacing={6}>
            <FormControl>
                <HStack mb={2}>
                <Icon as={MdOutlinePerson} boxSize={4} color={"gray.600"}/>
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
                <Icon as={FaPhone} boxSize={4} color={"gray.600"}/>
                <FormLabel mb={0}>Phone Number</FormLabel>
                </HStack>
                <Input type='tel'
                placeholder="Enter US phone number"
                value={phoneNumber}
                size={"lg"}
                onChange={(e) => setPhoneNumber(e.target.value)}
                variant={"filled"}/>
            </FormControl>
            <FormControl>
                <HStack mb={2}>
                <Icon as={MdOutlineMail} boxSize={4} color={"gray.600"}/>
                <FormLabel mb={0}>Email</FormLabel>
                </HStack>
                <Input type='text'
                placeholder="Enter Email"
                value={email}
                size={"lg"}
                onChange={(e) => setEmail(e.target.value)}
                variant={"filled"}/>
            </FormControl>

            <FormControl>
                <HStack mb={2}>
                <Icon as={FaLock} boxSize={4} color={"gray.600"}/>
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
            {/* confirm password */}
            <FormControl>
                <HStack mb={2}>
                <Icon as={FaLock} boxSize={4} color={"gray.600"}/>
                <FormLabel mb={0}>Confirm Password</FormLabel>
                </HStack>
                <InputGroup>
                    <Input
                    placeholder="Confirm password"
                    value={confirmPassword}
                    size={"lg"}
                    type={showPassword ? 'text' : 'password'}
                    onChange={(e) => setConfirmPassword(e.target.value)}
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
            <FormControl>
                <Checkbox
                size={"md"}
                isChecked={allowNotifications}
                onChange={(e) => setAllowNotifications(e.target.checked)}>
                    Enable SMS Text Notifications
                </Checkbox>
            </FormControl>
            
            
            <Button
            type="submit"
            isLoading={isLoading}
            bg={"brand.orange.400"}
            color={"brand.white.100"}
            fontWeight={"extrabold"}
            spinnerPlacement="start"
            w={"full"}
            p={6}
            onClick={handleRegister}>
                Register
            </Button>
            <Text>Already have an account? <ChakraLink as={ReactLink} to={"/login"}>Login</ChakraLink></Text>
            </VStack>
        </Box>
        </VStack>
        </>

    )
}