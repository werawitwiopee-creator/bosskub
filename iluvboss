-- สำหรับบอส ไอเลิฟยู 💜
-- วางใน StarterPlayerScripts

local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")

local player = Players.LocalPlayer
local playerGui = player:WaitForChild("PlayerGui")

-- ===== แปลง Decimal → Hex =====
local function toHex(num)
	local n = tonumber(num)
	if not n then return nil end
	n = math.floor(n)
	if n < 0 then return nil end
	return string.format("0x%X", n)
end

-- ===== ScreenGui =====
local screenGui = Instance.new("ScreenGui")
screenGui.Name = "HexCuteGui"
screenGui.ResetOnSpawn = false
screenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
screenGui.Parent = playerGui

-- ===== Main Frame =====
local mainFrame = Instance.new("Frame")
mainFrame.Name = "MainFrame"
mainFrame.Size = UDim2.new(0, 320, 0, 370)
mainFrame.Position = UDim2.new(0.5, -160, 0.5, -185)
mainFrame.BackgroundColor3 = Color3.fromRGB(255, 245, 252)
mainFrame.BorderSizePixel = 0
mainFrame.ClipsDescendants = true
mainFrame.Parent = screenGui

local mainCorner = Instance.new("UICorner")
mainCorner.CornerRadius = UDim.new(0, 24)
mainCorner.Parent = mainFrame

local mainStroke = Instance.new("UIStroke")
mainStroke.Thickness = 2.5
mainStroke.Color = Color3.fromRGB(255, 180, 220)
mainStroke.Parent = mainFrame

-- เงา
local shadow = Instance.new("Frame")
shadow.Size = UDim2.new(1, 16, 1, 16)
shadow.Position = UDim2.new(0, -8, 0, 8)
shadow.BackgroundColor3 = Color3.fromRGB(255, 160, 200)
shadow.BorderSizePixel = 0
shadow.ZIndex = mainFrame.ZIndex - 1
shadow.Parent = mainFrame

local shadowCorner = Instance.new("UICorner")
shadowCorner.CornerRadius = UDim.new(0, 28)
shadowCorner.Parent = shadow

local shadowGrad = Instance.new("UIGradient")
shadowGrad.Transparency = NumberSequence.new({
	NumberSequenceKeypoint.new(0, 0.6),
	NumberSequenceKeypoint.new(1, 1),
})
shadowGrad.Rotation = 90
shadowGrad.Parent = shadow

-- ===== Top pastel bar =====
local topBar = Instance.new("Frame")
topBar.Size = UDim2.new(1, 0, 0, 62)
topBar.Position = UDim2.new(0, 0, 0, 0)
topBar.BackgroundColor3 = Color3.fromRGB(255, 200, 230)
topBar.BorderSizePixel = 0
topBar.Parent = mainFrame

local topBarCorner = Instance.new("UICorner")
topBarCorner.CornerRadius = UDim.new(0, 24)
topBarCorner.Parent = topBar

local topBarFix = Instance.new("Frame")
topBarFix.Size = UDim2.new(1, 0, 0, 24)
topBarFix.Position = UDim2.new(0, 0, 1, -24)
topBarFix.BackgroundColor3 = Color3.fromRGB(255, 200, 230)
topBarFix.BorderSizePixel = 0
topBarFix.Parent = topBar

local topBarGrad = Instance.new("UIGradient")
topBarGrad.Color = ColorSequence.new({
	ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 210, 235)),
	ColorSequenceKeypoint.new(1, Color3.fromRGB(250, 185, 220)),
})
topBarGrad.Rotation = 90
topBarGrad.Parent = topBar

-- Title
local titleLabel = Instance.new("TextLabel")
titleLabel.Size = UDim2.new(1, -60, 1, 0)
titleLabel.Position = UDim2.new(0, 18, 0, 0)
titleLabel.BackgroundTransparency = 1
titleLabel.Text = "🌸  HEX ID TOOL"
titleLabel.TextColor3 = Color3.fromRGB(200, 80, 140)
titleLabel.TextSize = 17
titleLabel.Font = Enum.Font.GothamBold
titleLabel.TextXAlignment = Enum.TextXAlignment.Left
titleLabel.Parent = topBar

-- Watermark
local watermark = Instance.new("TextLabel")
watermark.Size = UDim2.new(1, -20, 0, 16)
watermark.Position = UDim2.new(0, 18, 0, 42)
watermark.BackgroundTransparency = 1
watermark.Text = "สำหรับบอส ไอเลิฟยู 💜"
watermark.TextColor3 = Color3.fromRGB(210, 120, 170)
watermark.TextSize = 10
watermark.Font = Enum.Font.Gotham
watermark.TextXAlignment = Enum.TextXAlignment.Left
watermark.Parent = mainFrame

-- Close button
local closeBtn = Instance.new("TextButton")
closeBtn.Size = UDim2.new(0, 30, 0, 30)
closeBtn.Position = UDim2.new(1, -44, 0, 16)
closeBtn.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
closeBtn.Text = "✕"
closeBtn.TextColor3 = Color3.fromRGB(255, 130, 170)
closeBtn.TextSize = 13
closeBtn.Font = Enum.Font.GothamBold
closeBtn.BorderSizePixel = 0
closeBtn.AutoButtonColor = false
closeBtn.Parent = mainFrame

local closeBtnCorner = Instance.new("UICorner")
closeBtnCorner.CornerRadius = UDim.new(1, 0)
closeBtnCorner.Parent = closeBtn

local closeBtnStroke = Instance.new("UIStroke")
closeBtnStroke.Thickness = 1.5
closeBtnStroke.Color = Color3.fromRGB(255, 180, 210)
closeBtnStroke.Parent = closeBtn

closeBtn.MouseEnter:Connect(function()
	TweenService:Create(closeBtn, TweenInfo.new(0.15), {
		BackgroundColor3 = Color3.fromRGB(255, 100, 140),
		TextColor3 = Color3.fromRGB(255, 255, 255),
	}):Play()
end)
closeBtn.MouseLeave:Connect(function()
	TweenService:Create(closeBtn, TweenInfo.new(0.15), {
		BackgroundColor3 = Color3.fromRGB(255, 255, 255),
		TextColor3 = Color3.fromRGB(255, 130, 170),
	}):Play()
end)
closeBtn.MouseButton1Click:Connect(function()
	TweenService:Create(mainFrame, TweenInfo.new(0.35, Enum.EasingStyle.Back, Enum.EasingDirection.In), {
		Size = UDim2.new(0, 320, 0, 0),
	}):Play()
	task.wait(0.4)
	screenGui:Destroy()
end)

-- ===== Helper: สร้าง input box =====
local function makeInput(yPos, labelText, placeholder, editable)
	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.new(1, -40, 0, 18)
	lbl.Position = UDim2.new(0, 20, 0, yPos)
	lbl.BackgroundTransparency = 1
	lbl.Text = labelText
	lbl.TextColor3 = Color3.fromRGB(220, 120, 170)
	lbl.TextSize = 11
	lbl.Font = Enum.Font.GothamBold
	lbl.TextXAlignment = Enum.TextXAlignment.Left
	lbl.Parent = mainFrame

	local bg = Instance.new("Frame")
	bg.Size = UDim2.new(1, -40, 0, 42)
	bg.Position = UDim2.new(0, 20, 0, yPos + 20)
	bg.BackgroundColor3 = Color3.fromRGB(255, 240, 248)
	bg.BorderSizePixel = 0
	bg.Parent = mainFrame

	local bgCorner = Instance.new("UICorner")
	bgCorner.CornerRadius = UDim.new(0, 12)
	bgCorner.Parent = bg

	local bgStroke = Instance.new("UIStroke")
	bgStroke.Thickness = 1.5
	bgStroke.Color = Color3.fromRGB(255, 190, 220)
	bgStroke.Parent = bg

	local box = Instance.new("TextBox")
	box.Size = UDim2.new(1, -20, 1, 0)
	box.Position = UDim2.new(0, 10, 0, 0)
	box.BackgroundTransparency = 1
	box.Text = ""
	box.PlaceholderText = placeholder
	box.PlaceholderColor3 = Color3.fromRGB(210, 170, 195)
	box.TextColor3 = Color3.fromRGB(180, 70, 130)
	box.TextSize = 14
	box.Font = Enum.Font.Code
	box.TextXAlignment = Enum.TextXAlignment.Left
	box.ClearTextOnFocus = false
	box.TextEditable = editable
	box.Parent = bg

	if editable then
		box.Focused:Connect(function()
			TweenService:Create(bgStroke, TweenInfo.new(0.2), {
				Color = Color3.fromRGB(255, 130, 180),
				Thickness = 2.5,
			}):Play()
			TweenService:Create(bg, TweenInfo.new(0.2), {
				BackgroundColor3 = Color3.fromRGB(255, 248, 252),
			}):Play()
		end)
		box.FocusLost:Connect(function()
			TweenService:Create(bgStroke, TweenInfo.new(0.2), {
				Color = Color3.fromRGB(255, 190, 220),
				Thickness = 1.5,
			}):Play()
			TweenService:Create(bg, TweenInfo.new(0.2), {
				BackgroundColor3 = Color3.fromRGB(255, 240, 248),
			}):Play()
		end)
	end

	return box, bgStroke, bg
end

-- ===== Input fields =====
local idBox = makeInput(72, "✦  USER ID (DECIMAL)", "ใส่ไอดีที่นี่เลยนะ~", true)
local hexBox, hexStroke, hexBg = makeInput(172, "✦  HEX ID", "ผลลัพธ์จะโผล่ตรงนี้ ♡", false)

-- ===== Helper: สร้างปุ่ม =====
local function makeButton(xOffset, width, yPos, icon, label, r, g, b)
	local btn = Instance.new("TextButton")
	btn.Size = UDim2.new(0, width, 0, 44)
	btn.Position = UDim2.new(0, xOffset, 0, yPos)
	btn.BackgroundColor3 = Color3.fromRGB(r, g, b)
	btn.Text = icon .. "  " .. label
	btn.TextColor3 = Color3.fromRGB(255, 255, 255)
	btn.TextSize = 13
	btn.Font = Enum.Font.GothamBold
	btn.BorderSizePixel = 0
	btn.AutoButtonColor = false
	btn.Parent = mainFrame

	local btnCorner = Instance.new("UICorner")
	btnCorner.CornerRadius = UDim.new(0, 14)
	btnCorner.Parent = btn

	local btnShadow = Instance.new("Frame")
	btnShadow.Size = UDim2.new(1, 0, 1, 4)
	btnShadow.Position = UDim2.new(0, 0, 0, 4)
	btnShadow.BackgroundColor3 = Color3.fromRGB(math.max(r-40,0), math.max(g-40,0), math.max(b-40,0))
	btnShadow.BorderSizePixel = 0
	btnShadow.ZIndex = btn.ZIndex - 1
	btnShadow.Parent = btn

	local btnShadowCorner = Instance.new("UICorner")
	btnShadowCorner.CornerRadius = UDim.new(0, 14)
	btnShadowCorner.Parent = btnShadow

	btn.MouseEnter:Connect(function()
		TweenService:Create(btn, TweenInfo.new(0.12), {
			BackgroundColor3 = Color3.fromRGB(
				math.min(r+20,255), math.min(g+20,255), math.min(b+20,255)
			),
		}):Play()
	end)
	btn.MouseLeave:Connect(function()
		TweenService:Create(btn, TweenInfo.new(0.12), {
			BackgroundColor3 = Color3.fromRGB(r, g, b),
		}):Play()
	end)

	return btn
end

local encodeBtn = makeButton(20, 130, 278, "🔮", "เข้ารหัส", 245, 120, 170)
local copyBtn   = makeButton(165, 135, 278, "🌸", "คัดลอก", 180, 130, 230)

-- ===== เดโค: หัวใจลอย =====
local hearts = {"♡", "✿", "•", "˚", "♡"}
for i, h in ipairs(hearts) do
	local deco = Instance.new("TextLabel")
	deco.BackgroundTransparency = 1
	deco.Text = h
	deco.TextColor3 = Color3.fromRGB(255, 190, 220)
	deco.TextSize = math.random(10, 16)
	deco.Font = Enum.Font.GothamBold
	deco.Size = UDim2.new(0, 20, 0, 20)
	deco.Position = UDim2.new(0, 220 + (i * 10), 0, 8)
	deco.BackgroundTransparency = 1
	deco.ZIndex = 5
	deco.Parent = topBar

	task.spawn(function()
		local t = i * 0.8
		local baseY = 8
		while deco.Parent do
			t = t + task.wait(0.03)
			deco.Position = UDim2.new(0, 220 + (i * 10), 0, baseY + math.sin(t * 1.2) * 4)
		end
	end)
end

-- ===== Logic: เข้ารหัส =====
local lastHex = ""

encodeBtn.MouseButton1Click:Connect(function()
	local result = toHex(idBox.Text)
	if result then
		lastHex = result
		hexBox.Text = result
		TweenService:Create(hexBg, TweenInfo.new(0.1), { BackgroundColor3 = Color3.fromRGB(230, 255, 245) }):Play()
		TweenService:Create(hexStroke, TweenInfo.new(0.1), { Color = Color3.fromRGB(100, 210, 160) }):Play()
		task.wait(0.5)
		TweenService:Create(hexBg, TweenInfo.new(0.3), { BackgroundColor3 = Color3.fromRGB(255, 240, 248) }):Play()
		TweenService:Create(hexStroke, TweenInfo.new(0.3), { Color = Color3.fromRGB(255, 190, 220) }):Play()
	else
		lastHex = ""
		hexBox.Text = ""
		TweenService:Create(hexBg, TweenInfo.new(0.1), { BackgroundColor3 = Color3.fromRGB(255, 230, 235) }):Play()
		TweenService:Create(hexStroke, TweenInfo.new(0.1), { Color = Color3.fromRGB(255, 120, 140) }):Play()
		task.wait(0.5)
		TweenService:Create(hexBg, TweenInfo.new(0.3), { BackgroundColor3 = Color3.fromRGB(255, 240, 248) }):Play()
		TweenService:Create(hexStroke, TweenInfo.new(0.3), { Color = Color3.fromRGB(255, 190, 220) }):Play()
	end
end)

-- ===== Logic: คัดลอก =====
copyBtn.MouseButton1Click:Connect(function()
	if lastHex ~= "" then
		hexBox:CaptureFocus()
		hexBox.SelectionStart = 1
		hexBox.CursorPosition = #hexBox.Text + 1

		local orig = copyBtn.Text
		copyBtn.Text = "✓  คัดลอกแล้ว!"
		TweenService:Create(copyBtn, TweenInfo.new(0.1), { BackgroundColor3 = Color3.fromRGB(100, 200, 150) }):Play()
		task.wait(1.5)
		copyBtn.Text = orig
		TweenService:Create(copyBtn, TweenInfo.new(0.2), { BackgroundColor3 = Color3.fromRGB(180, 130, 230) }):Play()
	else
		copyBtn.Text = "⚠ เข้ารหัสก่อนนะ~"
		task.wait(1.2)
		copyBtn.Text = "🌸  คัดลอก"
	end
end)

-- ===== Draggable =====
local dragging, dragStart, startPos = false, nil, nil

mainFrame.InputBegan:Connect(function(input)
	if input.UserInputType == Enum.UserInputType.MouseButton1 then
		dragging = true
		dragStart = input.Position
		startPos = mainFrame.Position
	end
end)
mainFrame.InputEnded:Connect(function(input)
	if input.UserInputType == Enum.UserInputType.MouseButton1 then
		dragging = false
	end
end)
UserInputService.InputChanged:Connect(function(input)
	if dragging and input.UserInputType == Enum.UserInputType.MouseMovement then
		local delta = input.Position - dragStart
		mainFrame.Position = UDim2.new(
			startPos.X.Scale, startPos.X.Offset + delta.X,
			startPos.Y.Scale, startPos.Y.Offset + delta.Y
		)
	end
end)

-- ===== Intro animation =====
mainFrame.Size = UDim2.new(0, 320, 0, 0)
mainFrame.Position = UDim2.new(0.5, -160, 0.5, -10)
TweenService:Create(mainFrame, TweenInfo.new(0.55, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {
	Size = UDim2.new(0, 320, 0, 370),
	Position = UDim2.new(0.5, -160, 0.5, -185),
}):Play()

-- ===== Pulse border =====
local t2 = 0
RunService.RenderStepped:Connect(function(dt)
	t2 = t2 + dt
	local alpha = (math.sin(t2 * 2) + 1) / 2
	mainStroke.Color = Color3.fromRGB(255, math.floor(160 + alpha * 40), math.floor(200 + alpha * 30))
end)
