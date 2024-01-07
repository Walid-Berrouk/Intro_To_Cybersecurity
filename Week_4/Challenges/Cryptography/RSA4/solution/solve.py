import gmpy2
from Crypto.Util.number import long_to_bytes

n =74764076427399263976519125708303951775494707028675044478613975701977666807706222674963772861100506229203124351529097899151655103229375492355986410651780090818827179510455704306070201243037305775858898807534254756759670494509955585125638067559099010442972157084530964650598719659735673541307440411864766680553
c =27580632175660412352178793104334216554558395829267657090269987135659626618153614221019067030674427398763213994285995306480275173862442003136763512890164823549048528692570317128659005318514903130602230215156421420675681040443357893333729971871492582324063712033940601721553135783813294496270307035269524249314
e =65537
eq =2786478663387412812509043444880527852528818995060968909425036294184333160537016134983599362210509078725867241185574423460396551622529511977184782620080920614860028553441386561767821486203115967024774984703159873277560738861426851144628248337227237917878099622841004796183983916497817404979385789905886581760242512935111976648030318970119172743746301779993911833735833318560497909655372009627004132322959301543652307182529522945800884982615793444760286426240607521267490803119578566553403096078612666313439554397212327869739784782563001515631772216600860246477883205796664131638115589555614213987982201223159654858541171454539004218366457384295870341891544464289253698202210350304434443316526381089426639903024508205193454526048080677662700306273024757532359161527925758352715098868779015598253581338218012265287205813648030095432531869648544033814233034971162797417225017012075627115114806294878167091630283663879151438631184617870681161947718012977803108872874516746280068508229372642548547668751993094419320162855871863068604973882048297229417702230270156224108718547000343345887695778802349369557070330924502605258179321178561213270453120925515430156167437463475994243433151672234105772863643992281549044031624371890617507157817581916865882278668212503927040792267769920222373808833909527500796235615791719475838468338635676216509430232345976019639415762350238842584956111780039026384502936937447740128367060523224972575212413417331655650565445705291354272027639099424737898434130110986612055394052130304202845213865907458499743271617376

q= gmpy2.iroot(eq%n,2)[0]
p= n//q

phi = (p-1) * (q-1)

d = pow(e,-1,phi)

dec = pow(c,d,n)


print(long_to_bytes(dec))