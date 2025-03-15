local UserInputService = game:GetService("UserInputService")
local Players = game:GetService("Players")
local LocalPlayer = Players.LocalPlayer
local Camera = game:GetService("Workspace").CurrentCamera
local RunService = game:GetService("RunService")

-- Variables para activar/desactivar
local aimbotActive = false
local aimAssistActive = false
local espActive = false  
local isWalkSpeedEnabled = false  -- WalkSpeed (movimiento constante hacia adelante)

-- Tabla para almacenar los cuadros ESP de los jugadores
local playerBoxes = {}

-- Función para encontrar el objetivo más cercano (Aimbot)
local function getClosestTarget()
    local closestTarget = nil
    local shortestDistance = math.huge  

    for _, player in ipairs(Players:GetPlayers()) do
        if player ~= LocalPlayer and player.Character and player.Character:FindFirstChild("HumanoidRootPart") then
            local target = player.Character.HumanoidRootPart
            local distance = (Camera.CFrame.Position - target.Position).magnitude

            if distance < shortestDistance then
                closestTarget = target
                shortestDistance = distance
            end
        end
    end

    return closestTarget
end

-- Funciones de toggle
local function toggleAimbot()
    aimbotActive = not aimbotActive
    print("Aimbot activado:", aimbotActive)
end

local function toggleAimAssist()
    aimAssistActive = not aimAssistActive
    print("Aim Assist activado:", aimAssistActive)
end

local function toggleESP()
    espActive = not espActive
    print("ESP activado:", espActive)
end

local function toggleWalkSpeed()
    isWalkSpeedEnabled = not isWalkSpeedEnabled
    local character = LocalPlayer.Character
    local humanoid = character and character:FindFirstChild("Humanoid")

    if humanoid then
        humanoid.WalkSpeed = isWalkSpeedEnabled and 16
    end
end

-- Detectar cuando se presionan las teclas Z, X, C y V
UserInputService.InputBegan:Connect(function(input, gameProcessed)
    if gameProcessed then return end  

    if input.UserInputType == Enum.UserInputType.Keyboard then
        if input.KeyCode == Enum.KeyCode.Z then
            toggleAimbot()
        elseif input.KeyCode == Enum.KeyCode.X then
            toggleAimAssist()
        elseif input.KeyCode == Enum.KeyCode.C then
            toggleESP()
        elseif input.KeyCode == Enum.KeyCode.V then
            toggleWalkSpeed()
        end
    end
end)

-- Lógica principal para Aimbot, Aim Assist, ESP y WalkSpeed
RunService.RenderStepped:Connect(function()
    -- Aimbot
    if aimbotActive then
        local target = getClosestTarget()
        if target then
            local direction = (target.Position - Camera.CFrame.Position).unit
            Camera.CFrame = CFrame.new(Camera.CFrame.Position, Camera.CFrame.Position + direction)
        end
    end

    -- Aim Assist
    if aimAssistActive then
        local target = getClosestTarget()
        if target then
            local direction = (target.Position - Camera.CFrame.Position).unit
            Camera.CFrame = CFrame.new(Camera.CFrame.Position, Camera.CFrame.Position + direction * 0.9)
        end
    end

    -- ESP
    if espActive then
        for _, player in ipairs(Players:GetPlayers()) do
            if player ~= LocalPlayer and player.Character and player.Character:FindFirstChild("HumanoidRootPart") then
                local humanoidRootPart = player.Character.HumanoidRootPart
                local screenPosition, onScreen = Camera:WorldToScreenPoint(humanoidRootPart.Position)

                if onScreen then
                    if not playerBoxes[player] then
                        local box = Drawing.new("Square")
                        box.Visible = false
                        box.Color = Color3.fromRGB(255, 0, 0)  
                        box.Thickness = 2
                        box.Transparency = 1
                        playerBoxes[player] = box
                    end

                    local box = playerBoxes[player]
                    box.Position = Vector2.new(screenPosition.X - 25, screenPosition.Y - 25)
                    box.Size = Vector2.new(50, 50)
                    box.Visible = true
                end
            end
        end
    else
        for _, box in pairs(playerBoxes) do
            box.Visible = false
        end
    end

    -- WalkSpeed (movimiento constante hacia adelante)
    local character = LocalPlayer.Character
    local humanoidRootPart = character and character:FindFirstChild("HumanoidRootPart")
    
    if isWalkSpeedEnabled and humanoidRootPart then
        humanoidRootPart.CFrame = humanoidRootPart.CFrame + humanoidRootPart.CFrame.lookVector * 2
    end
end)
