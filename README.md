# GTN750 and autopilot mod for FYCYC C919

This is a mod for FYCYC C919 and should not be seen as a part of the product. Special thanks to [pysimconnect](https://github.com/patricksurry/pysimconnect).

## Prerequisite

[FYCYC-C919X (**still in its early stages**)](https://fycyc.com/)

[PMS50 GTN750](https://pms50.com/msfs/)

[MSFS Layout Generator](https://github.com/HughesMDflyer4/MSFSLayoutGenerator)

[Python](https://www.python.org/)

## How to install

**Manual installation is required! MAKE BACKUP before any file edit!**

1. Downlaod PMS50 GTN750 [here](https://pms50.com/msfs/downloads/gtn750-basic/) and follow its [Installation instructions](https://pms50.com/fs2020/gtn750/documentation.pdf)

2. Follow the integration guide (`<Community Folder>\pms50-instrument-gtn750\Integration\integration.pdf`). Steps include

- Copy `<Community Folder>\pms50-instrument-gtn750\Integration\Files\interface\pms_gtn750_int` to `<Community Folder>\fycyc-aircraft-c919x\html_ui\Pages\VCockpit\Instruments\NavSystems\fycyc-aircraft-c919x\pms_gtn750_int`. Create parent folders if neccesery.

- Edit `<Community Folder>\fycyc-aircraft-c919x\SimObjects\Airplanes\fycyc_aircraft_c919\panel\panel.cfg` file. Add these lines to the bottom.

   ```plain
   [Vcockpit16]
   size_mm=650,768
   pixel_size=650,768
   texture=$GTN750_screen
   htmlgauge00=NavSystems/fycyc-aircraft-c919x/pms50_gtn750_int/gtn750_int.html, 0, 0, 650,768
   
   [Vcockpit17]
   size_mm=650,768
   pixel_size=650,768
   texture=$GTN750_screen2
   htmlgauge00=NavSystems/fycyc-aircraft-c919x/pms50_gtn750_int/gtn750_int.html?index=2, 0, 0, 650,768
   
   [VCockpit18]
   size_mm=0,0
   pixel_size=0,0
   texture=$NONE
   background_color=42,42,40
   htmlgauge00= NavSystems/fycyc-aircraft-c919x/pms50_gtn750_int/AP1.html, 0,0,0,0
   
   [VCockpit19]
   size_mm=0,0
   pixel_size=0,0
   texture=$NONE
   background_color=42,42,40
   htmlgauge00= NavSystems/fycyc-aircraft-c919x/pms50_gtn750_int/AP2.html, 0,0,0,0
   ```

- Copy `<Community Folder>\pms50-instrument-gtn750\Integration\Files\sounds\button_gtn750.wav` to `<Community Folder>\fycyc-aircraft-c919x\SimObjects\Airplanes\fycyc_aircraft_c919\sound\button_gtn750.wav`.

- Edit `<Community Folder>\fycyc-aircraft-c919x\SimObjects\Airplanes\fycyc_aircraft_c919\sound\sound.xml` file. Replace

   ```plain
   		<Sound WwiseData="true" WwiseEvent="wipers_backward" NodeName="WIPER_BASE_L"/>
   	</AnimationSounds>
   ```

   with

   ```plain
   		<Sound WwiseData="true" WwiseEvent="wipers_backward" NodeName="WIPER_BASE_L"/>
   		<Sound WwiseData="false" WwiseEvent="custom_sound_12" FileName="button_gtn750" ViewPoint="Inside"/>
   	</AnimationSounds>
   ```

- Copy GTN750 model and texture files in `models` folder to `<Community Folder>\fycyc-aircraft-c919x\SimObjects\Airplanes\fycyc_aircraft_c919`

- Edit `<Community Folder>\fycyc-aircraft-c919x\SimObjects\Airplanes\fycyc_aircraft_c919\model\C919X_Interior.xml`. replace

   ```plain
   <ModelInfo>
   	<LODS>
   		<LOD minSize="50" ModelFile="C919X_Interior.gltf">
   			<MergeModel>C919X_Interior_Cabin.gltf</MergeModel>
   			<MergeModel>C919X_Interior_Seat.gltf</MergeModel>
   		</LOD>
   	</LODS>
   
   	<Behaviors>
   		<Include ModelBehaviorFile="FYCYC_C919X_Templates.xml"/>
   ```

   with

   ```plain
   <ModelInfo>
   	<LODS>
   		<LOD minSize="50" ModelFile="C919X_Interior.gltf">
   			<MergeModel>C919X_Interior_Cabin.gltf</MergeModel>
   			<MergeModel>C919X_Interior_Seat.gltf</MergeModel>
   			<MergeModel>GTN750.gltf</MergeModel>
   		</LOD>
   	</LODS>
   
   	<Behaviors>
   <Include Path="Asobo\Common.xml"/>
   <!-- PMS50 GTN750 -->
   <Component ID="GTN750_Vol" Node="GTN750_Vol">
       <UseTemplate Name="ASOBO_GT_Knob_Infinite_Push_Timed">
           <ANIM_NAME_KNOB>GTN750_Vol</ANIM_NAME_KNOB>
           <ANIM_NAME_PUSH>GTN750_VolPush</ANIM_NAME_PUSH>
           <CLOCKWISE_CODE>(&gt;H:GTN750_VolInc)</CLOCKWISE_CODE>
           <ANTICLOCKWISE_CODE>(&gt;H:GTN750_VolDec)</ANTICLOCKWISE_CODE>
           <LEFT_SINGLE_CODE>(&gt;H:GTN750_VolPush)</LEFT_SINGLE_CODE>
       </UseTemplate>
   </Component>
   <Component ID="GTN750_KnobSmall" Node="GTN750_KnobSmall">
       <UseTemplate Name="ASOBO_GT_Knob_Infinite_Push_Timed">
           <ANIM_NAME_KNOB>GTN750_KnobSmall</ANIM_NAME_KNOB>
           <ANIM_NAME_PUSH>GTN750_KnobSmallPush</ANIM_NAME_PUSH>
           <CLOCKWISE_CODE>(&gt;H:GTN750_KnobSmallInc)</CLOCKWISE_CODE>
           <ANTICLOCKWISE_CODE>(&gt;H:GTN750_KnobSmallDec)</ANTICLOCKWISE_CODE>
           <SHORT_CLICK_CODE>(&gt;H:GTN750_KnobPush)</SHORT_CLICK_CODE>
           <LONG_CLICK_CODE>(&gt;H:GTN750_KnobPushLong)</LONG_CLICK_CODE>
           <LONG_CLICK_TIME>1</LONG_CLICK_TIME>
       </UseTemplate>
   </Component>
   <Component ID="GTN750_KnobLarge" Node="GTN750_KnobLarge">
       <UseTemplate Name="ASOBO_GT_Knob_Infinite">
           <ANIM_NAME>GTN750_KnobLarge</ANIM_NAME>
           <CLOCKWISE_CODE>(&gt;H:GTN750_KnobLargeInc)</CLOCKWISE_CODE>
           <ANTICLOCKWISE_CODE>(&gt;H:GTN750_KnobLargeDec)</ANTICLOCKWISE_CODE>
       </UseTemplate>
   </Component>
   <Component ID="GTN750_HomePush" Node="GTN750_HomePush">
       <UseTemplate Name="ASOBO_GT_Push_Button_Timed">
           <ANIM_NAME>GTN750_HomePush</ANIM_NAME>
           <SHORT_CLICK_CODE>(&gt;H:GTN750_HomePush)</SHORT_CLICK_CODE>
           <LONG_CLICK_CODE>(&gt;H:GTN750_HomePushLong)</LONG_CLICK_CODE>
       </UseTemplate>
   </Component>
   <Component ID="GTN750_DirectToPush" Node="GTN750_DirectToPush">
       <UseTemplate Name="ASOBO_GT_Push_Button">
           <ANIM_NAME>GTN750_DirectToPush</ANIM_NAME>
           <LEFT_SINGLE_CODE>(&gt;H:GTN750_DirectToPush)</LEFT_SINGLE_CODE>
       </UseTemplate>
   </Component>
   
   <Component ID="GTN750_Vol2" Node="GTN750_Vol2">
       <UseTemplate Name="ASOBO_GT_Knob_Infinite_Push_Timed">
           <ANIM_NAME_KNOB>GTN750_Vol</ANIM_NAME_KNOB>
           <ANIM_NAME_PUSH>GTN750_VolPush</ANIM_NAME_PUSH>
           <CLOCKWISE_CODE>(&gt;H:GTN750_2_VolInc)</CLOCKWISE_CODE>
           <ANTICLOCKWISE_CODE>(&gt;H:GTN750_2_VolDec)</ANTICLOCKWISE_CODE>
           <LEFT_SINGLE_CODE>(&gt;H:GTN750_2_VolPush)</LEFT_SINGLE_CODE>
       </UseTemplate>
   </Component>
   <Component ID="GTN750_KnobSmall2" Node="GTN750_KnobSmall2">
       <UseTemplate Name="ASOBO_GT_Knob_Infinite_Push_Timed">
           <ANIM_NAME_KNOB>GTN750_KnobSmall</ANIM_NAME_KNOB>
           <ANIM_NAME_PUSH>GTN750_KnobSmallPush</ANIM_NAME_PUSH>
           <CLOCKWISE_CODE>(&gt;H:GTN750_2_KnobSmallInc)</CLOCKWISE_CODE>
           <ANTICLOCKWISE_CODE>(&gt;H:GTN750_2_KnobSmallDec)</ANTICLOCKWISE_CODE>
           <SHORT_CLICK_CODE>(&gt;H:GTN750_2_KnobPush)</SHORT_CLICK_CODE>
           <LONG_CLICK_CODE>(&gt;H:GTN750_2_KnobPushLong)</LONG_CLICK_CODE>
           <LONG_CLICK_TIME>1</LONG_CLICK_TIME>
       </UseTemplate>
   </Component>
   <Component ID="GTN750_KnobLarge2" Node="GTN750_KnobLarge2">
       <UseTemplate Name="ASOBO_GT_Knob_Infinite">
           <ANIM_NAME>GTN750_KnobLarge</ANIM_NAME>
           <CLOCKWISE_CODE>(&gt;H:GTN750_2_KnobLargeInc)</CLOCKWISE_CODE>
           <ANTICLOCKWISE_CODE>(&gt;H:GTN750_2_KnobLargeDec)</ANTICLOCKWISE_CODE>
       </UseTemplate>
   </Component>
   <Component ID="GTN750_HomePush2" Node="GTN750_HomePush2">
       <UseTemplate Name="ASOBO_GT_Push_Button_Timed">
           <ANIM_NAME>GTN750_HomePush</ANIM_NAME>
           <SHORT_CLICK_CODE>(&gt;H:GTN750_2_HomePush)</SHORT_CLICK_CODE>
           <LONG_CLICK_CODE>(&gt;H:GTN750_2_HomePushLong)</LONG_CLICK_CODE>
       </UseTemplate>
   </Component>
   <Component ID="GTN750_DirectToPush2" Node="GTN750_DirectToPush2">
       <UseTemplate Name="ASOBO_GT_Push_Button">
           <ANIM_NAME>GTN750_DirectToPush</ANIM_NAME>
           <LEFT_SINGLE_CODE>(&gt;H:GTN750_2_DirectToPush)</LEFT_SINGLE_CODE>
       </UseTemplate>
   </Component>
   
   		<Include ModelBehaviorFile="FYCYC_C919X_Templates.xml"/>
   ```

3. Edit  `<Community Folder>\pms50-instrument-gtn750\html_ui\Pms50\gtn750\Pages\VCockpit\Instruments\Shared\WT\v2\msfssdk.js` file. Replace all occurrences of `'INDICATED AlTITUDE'` with `'INDICATED AlTITUDE:2'`, so that the altitude read by autopilot comes from the altimeter on captain side.

4. Copy MSFSLayoutGenerator.exe to `<Community Folder>\fycyc-aircraft-c919x\`. Drag and drop `layout.json` file on the exe file to regenerate it.

5. See the code in `autopilot` folder if you want to use autopilot!