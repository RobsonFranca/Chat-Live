from app.ui.config_window import ConfigWindow

app = ConfigWindow()
app.mainloop()

# testando a parte de emotes
# from tkinter import Tk

# from app.twitch.emote import Emote

# app = Tk()
# em = Emote("emotesv2_4ea6b9356c584185911caa28385b0eb9", "0-6")
# em.get_tk_image(app)

# testando a parte de mensagens
# from app.twitch.message import Message
# m = message = Message("@badge-info=subscriber/1;badges=subscriber/0,sub-gifter/1;client-nonce=50bfecd245d74d429e36478c1c610504;color=#D6A3F3;display-name=xkxixaxm_;emotes=emotesv2_024b9fc4003244caa1ac123a611a6ad1:11-22,24-35;first-msg=0;flags=;id=693c4d90-6152-4d43-92ae-c9de4664cbdd;mod=0;returning-chatter=0;room-id=106125366;subscriber=1;tmi-sent-ts=1780282135895;turbo=0;user-id=834338740;user-type= :xkxixaxm_!xkxixaxm_@xkxixaxm_.tmi.twitch.tv PRIVMSG #alexisdino :aninha god xdinoLovezin xdinoLovezin")
# print(m.message)